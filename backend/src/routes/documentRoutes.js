import express from 'express';
import crypto from 'crypto';
import { upload } from '../middleware/uploadMiddleware.js';
import { documentRepository } from '../repositories/documentRepository.js';
import { extractDocumentText } from '../document-processing/extractors.js';
import { chunkDocumentPages } from '../document-processing/chunker.js';
import { vectorStore } from '../retrieval/vector_store.js';

const router = express.Router();

/**
 * GET /api/documents — List all documents
 */
router.get('/', async (req, res, next) => {
  try {
    const docs = await documentRepository.getAllDocuments();
    res.json({
      success: true,
      documents: docs
    });
  } catch (err) {
    next(err);
  }
});

/**
 * GET /api/documents/:id — Get document details and all versions
 */
router.get('/:id', async (req, res, next) => {
  try {
    const doc = await documentRepository.getDocumentById(req.params.id);
    if (!doc) {
      return res.status(404).json({ success: false, error: 'Document not found' });
    }
    const versions = await documentRepository.getVersionsByDocumentId(doc.id);
    res.json({
      success: true,
      document: doc,
      versions
    });
  } catch (err) {
    next(err);
  }
});

/**
 * POST /api/documents/upload — Ingest new document or new version
 */
router.post('/upload', upload.single('file'), async (req, res, next) => {
  try {
    if (!req.file) {
      return res.status(400).json({ success: false, error: 'No file uploaded' });
    }

    const {
      title,
      category = 'General',
      versionNumber = '1.0',
      status = 'Active',
      effectiveDate,
      expirationDate,
      description,
      groupId,
      documentId
    } = req.body;

    const file = req.file;

    // 1. Resolve Document Group
    let resolvedGroupId = groupId;
    if (!resolvedGroupId) {
      resolvedGroupId = `grp_${crypto.randomBytes(6).toString('hex')}`;
      await documentRepository.createGroup({
        id: resolvedGroupId,
        name: title || file.originalname,
        description: description || 'Document group created via upload',
        category: category || 'General',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      });
    }

    // 2. Resolve Document ID
    let resolvedDocId = documentId;
    if (!resolvedDocId) {
      resolvedDocId = `doc_${crypto.randomBytes(6).toString('hex')}`;
      await documentRepository.createDocument({
        id: resolvedDocId,
        group_id: resolvedGroupId,
        title: title || file.originalname,
        category: category || 'General',
        created_at: new Date().toISOString()
      });
    }

    // 3. Create Version Record
    const versionId = `ver_${crypto.randomBytes(6).toString('hex')}`;
    const newVersion = {
      id: versionId,
      document_id: resolvedDocId,
      group_id: resolvedGroupId,
      version_number: versionNumber || '1.0',
      status: status || 'Draft',
      file_name: file.originalname,
      file_path: file.path,
      file_size: file.size,
      mime_type: file.mimetype,
      checksum: crypto.createHash('sha256').update(file.filename).digest('hex'),
      effective_date: effectiveDate || null,
      expiration_date: expirationDate || null,
      description: description || null,
      uploaded_at: new Date().toISOString(),
      processing_status: 'Processing',
      error_message: null
    };

    await documentRepository.createVersion(newVersion);

    // 4. Create Processing Job
    const jobId = `job_${crypto.randomBytes(6).toString('hex')}`;
    await documentRepository.createProcessingJob({
      id: jobId,
      version_id: versionId,
      status: 'In Progress',
      progress: 10,
      step: 'File uploaded, beginning text extraction',
      error_message: null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    });

    // 5. Execute processing asynchronously
    processDocumentPipeline(jobId, newVersion, title || file.originalname);

    res.status(201).json({
      success: true,
      message: 'Document uploaded successfully. Processing started.',
      jobId,
      documentId: resolvedDocId,
      versionId
    });
  } catch (err) {
    next(err);
  }
});

/**
 * DELETE /api/documents/:id — Delete document and associated vectors
 */
router.delete('/:id', async (req, res, next) => {
  try {
    const docId = req.params.id;
    await vectorStore.deleteByDocumentId(docId);
    await documentRepository.deleteDocument(docId);
    res.json({
      success: true,
      message: 'Document and all its indexed vector chunks deleted successfully.'
    });
  } catch (err) {
    next(err);
  }
});

/**
 * Asynchronous Background Pipeline: Extraction -> Chunking -> Vector Indexing
 */
async function processDocumentPipeline(jobId, version, documentTitle) {
  try {
    // Step 1: Extraction
    await documentRepository.updateProcessingJob(jobId, { progress: 30, step: 'Extracting text and page boundaries...' });
    const extractResult = await extractDocumentText(version.file_path, version.mime_type, version.file_name);

    if (!extractResult.success) {
      await documentRepository.updateVersionProcessing(version.id, 'Failed', extractResult.error);
      await documentRepository.updateProcessingJob(jobId, { status: 'Failed', progress: 100, error_message: extractResult.error });
      return;
    }

    // Step 2: Semantic Chunking
    await documentRepository.updateProcessingJob(jobId, { progress: 60, step: 'Creating semantic chunks with page tags...' });
    const chunks = chunkDocumentPages(extractResult.pages, {
      versionId: version.id,
      documentId: version.document_id,
      groupId: version.group_id,
      documentTitle,
      versionNumber: version.version_number,
      status: version.status,
      effectiveDate: version.effective_date,
      expirationDate: version.expiration_date
    });

    // Save Chunks to Database
    await documentRepository.saveChunks(chunks);

    // Step 3: Embeddings & Vector Storage
    await documentRepository.updateProcessingJob(jobId, { progress: 85, step: 'Generating local embeddings and vector indexing...' });
    await vectorStore.indexChunks(chunks);

    // Step 4: Complete
    await documentRepository.updateVersionProcessing(version.id, 'Indexed', null);
    await documentRepository.updateProcessingJob(jobId, { status: 'Completed', progress: 100, step: `Indexing complete. ${chunks.length} chunks generated.` });
  } catch (err) {
    console.error('❌ Pipeline processing failed:', err.message);
    await documentRepository.updateVersionProcessing(version.id, 'Failed', err.message);
    await documentRepository.updateProcessingJob(jobId, { status: 'Failed', progress: 100, error_message: err.message });
  }
}

export default router;
