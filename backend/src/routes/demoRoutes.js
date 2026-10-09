import express from 'express';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { config } from '../config/env.js';
import { documentRepository } from '../repositories/documentRepository.js';
import { chunkDocumentPages } from '../document-processing/chunker.js';
import { vectorStore } from '../retrieval/vector_store.js';

const router = express.Router();

/**
 * POST /api/demo/seed-leave-policy — Ingest the 3-version hackathon test scenario
 */
router.post('/seed-leave-policy', async (req, res, next) => {
  try {
    const groupId = 'grp_leave_policy_demo';
    const docId = 'doc_leave_policy_demo';

    // 1. Create or ensure Group & Document
    await documentRepository.createGroup({
      id: groupId,
      name: 'Employee Annual Leave Policy',
      description: 'Official corporate policy for annual leave entitlements and vacation accrual.',
      category: 'Human Resources',
      created_at: new Date('2021-01-01').toISOString(),
      updated_at: new Date('2025-01-01').toISOString()
    });

    await documentRepository.createDocument({
      id: docId,
      group_id: groupId,
      title: 'Annual Leave Policy Manual',
      category: 'Human Resources',
      created_at: new Date('2021-01-01').toISOString()
    });

    // 2. Prepare Version 1 (2021 - Superseded: 15 days)
    const v1Path = path.join(config.storageDir, 'Leave_Policy_v1.0.txt');
    const v1Text = `COMPANY ANNUAL LEAVE POLICY (VERSION 1.0 - EFFECTIVE JAN 2021)\n\nSection 1: General Entitlement\nAll full-time employees are entitled to an annual leave allowance of 15 days per calendar year. Unused leave expires at year-end.\n\nSection 2: Carryover Rules\nEmployees may not carry over unused vacation days into subsequent fiscal years.`;
    fs.writeFileSync(v1Path, v1Text, 'utf8');

    const v1 = {
      id: 'ver_leave_v1',
      document_id: docId,
      group_id: groupId,
      version_number: '1.0',
      status: 'Superseded',
      file_name: 'Leave_Policy_v1.0.txt',
      file_path: v1Path,
      file_size: Buffer.byteLength(v1Text),
      mime_type: 'text/plain',
      checksum: crypto.createHash('sha256').update(v1Text).digest('hex'),
      effective_date: '2021-01-01',
      expiration_date: '2022-12-31',
      description: 'Initial leave policy established in 2021.',
      uploaded_at: new Date('2021-01-05').toISOString(),
      processing_status: 'Indexed',
      error_message: null
    };
    await documentRepository.createVersion(v1);
    const v1Chunks = chunkDocumentPages([{ pageNumber: 1, text: v1Text }], {
      versionId: v1.id,
      documentId: docId,
      groupId,
      documentTitle: 'Annual Leave Policy Manual',
      versionNumber: '1.0',
      status: 'Superseded',
      effectiveDate: '2021-01-01',
      expirationDate: '2022-12-31'
    });
    await documentRepository.saveChunks(v1Chunks);
    await vectorStore.indexChunks(v1Chunks);

    // 3. Prepare Version 2 (2023 - Superseded: 18 days)
    const v2Path = path.join(config.storageDir, 'Leave_Policy_v2.0.txt');
    const v2Text = `COMPANY ANNUAL LEAVE POLICY (VERSION 2.0 - EFFECTIVE JAN 2023)\n\nSection 1: General Entitlement\nUnder the revised 2023 guidelines, all full-time employees are entitled to an annual leave allowance of 18 days per calendar year.\n\nSection 2: Carryover Rules\nA maximum of 3 unused leave days may be carried over into the first quarter of the new year with supervisor approval.`;
    fs.writeFileSync(v2Path, v2Text, 'utf8');

    const v2 = {
      id: 'ver_leave_v2',
      document_id: docId,
      group_id: groupId,
      version_number: '2.0',
      status: 'Superseded',
      file_name: 'Leave_Policy_v2.0.txt',
      file_path: v2Path,
      file_size: Buffer.byteLength(v2Text),
      mime_type: 'text/plain',
      checksum: crypto.createHash('sha256').update(v2Text).digest('hex'),
      effective_date: '2023-01-01',
      expiration_date: '2024-12-31',
      description: 'Updated leave allowance for 2023 fiscal cycle.',
      uploaded_at: new Date('2023-01-10').toISOString(),
      processing_status: 'Indexed',
      error_message: null
    };
    await documentRepository.createVersion(v2);
    const v2Chunks = chunkDocumentPages([{ pageNumber: 1, text: v2Text }], {
      versionId: v2.id,
      documentId: docId,
      groupId,
      documentTitle: 'Annual Leave Policy Manual',
      versionNumber: '2.0',
      status: 'Superseded',
      effectiveDate: '2023-01-01',
      expirationDate: '2024-12-31'
    });
    await documentRepository.saveChunks(v2Chunks);
    await vectorStore.indexChunks(v2Chunks);

    // 4. Prepare Version 3 (2025 - Active: 20 days)
    const v3Path = path.join(config.storageDir, 'Leave_Policy_v3.0.txt');
    const v3Text = `COMPANY ANNUAL LEAVE POLICY (VERSION 3.0 - EFFECTIVE JAN 2025 - CURRENT ACTIVE)\n\nSection 1: General Entitlement\nCommencing January 1, 2025, all full-time employees receive an annual leave allowance of 20 days per calendar year.\n\nSection 2: Carryover Rules\nEmployees may carry over up to 5 unused days into the next calendar year.\n\nSection 3: Emergency Leave\nEmployees are granted 3 emergency personal days in addition to standard annual leave.`;
    fs.writeFileSync(v3Path, v3Text, 'utf8');

    const v3 = {
      id: 'ver_leave_v3',
      document_id: docId,
      group_id: groupId,
      version_number: '3.0',
      status: 'Active',
      file_name: 'Leave_Policy_v3.0.txt',
      file_path: v3Path,
      file_size: Buffer.byteLength(v3Text),
      mime_type: 'text/plain',
      checksum: crypto.createHash('sha256').update(v3Text).digest('hex'),
      effective_date: '2025-01-01',
      expiration_date: null,
      description: 'Current active leave policy reflecting 20-day allowance.',
      uploaded_at: new Date('2025-01-02').toISOString(),
      processing_status: 'Indexed',
      error_message: null
    };
    await documentRepository.createVersion(v3);
    const v3Chunks = chunkDocumentPages([{ pageNumber: 1, text: v3Text }], {
      versionId: v3.id,
      documentId: docId,
      groupId,
      documentTitle: 'Annual Leave Policy Manual',
      versionNumber: '3.0',
      status: 'Active',
      effectiveDate: '2025-01-01',
      expirationDate: null
    });
    await documentRepository.saveChunks(v3Chunks);
    await vectorStore.indexChunks(v3Chunks);

    res.json({
      success: true,
      message: 'Demo dataset successfully seeded with v1.0 (15 days - Superseded), v2.0 (18 days - Superseded), and v3.0 (20 days - Active).',
      documentId: docId,
      versions: ['1.0', '2.0', '3.0']
    });
  } catch (err) {
    next(err);
  }
});

/**
 * POST /api/demo/reset — Safely clear demo data
 */
router.post('/reset', async (req, res, next) => {
  try {
    await vectorStore.resetAll();
    const store = documentRepository.db ? documentRepository.db.getLocalStore() : null;
    if (store) {
      store.document_groups = [];
      store.documents = [];
      store.document_versions = [];
      store.document_chunks = [];
      store.processing_jobs = [];
      store.messages = [];
      documentRepository.db.persistLocal();
    }
    res.json({
      success: true,
      message: 'Repository reset. Ready for clean ingestion.'
    });
  } catch (err) {
    next(err);
  }
});

export default router;
