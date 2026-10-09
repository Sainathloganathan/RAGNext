import express from 'express';
import crypto from 'crypto';
import { documentRepository } from '../repositories/documentRepository.js';
import { vectorStore } from '../retrieval/vector_store.js';
import { versionRules } from '../rag/version_rules.js';
import { generateGroundedAnswer } from '../rag/answer_generator.js';

const router = express.Router();

/**
 * POST /api/chat — Execute Version-Aware RAG query
 */
router.post('/', async (req, res, next) => {
  try {
    const {
      question,
      documentId = null,
      category = null,
      statusFilter = null,
      conversationId = null
    } = req.body;

    if (!question || !question.trim()) {
      return res.status(400).json({ success: false, error: 'Question cannot be empty' });
    }

    const startTime = Date.now();

    // 1. Classify Query Intent (CURRENT, HISTORICAL, COMPARISON)
    const intentInfo = versionRules.classifyQueryIntent(question);

    // 2. Fetch all document versions from database
    let allVersions = [];
    if (documentId) {
      allVersions = await documentRepository.getVersionsByDocumentId(documentId);
    } else {
      const allDocs = await documentRepository.getAllDocuments();
      for (const d of allDocs) {
        const vers = await documentRepository.getVersionsByDocumentId(d.id);
        allVersions.push(...vers);
      }
    }

    // 3. Resolve eligible versions based on version rules & intent
    const { eligibleVersions, conflictWarning, statusNote } = versionRules.resolveEligibleVersions(allVersions, intentInfo);
    const eligibleVersionIds = eligibleVersions.map(v => v.id);

    // 4. Retrieve semantically matching chunks from vector database
    let retrievedChunks = [];
    if (eligibleVersionIds.length > 0) {
      retrievedChunks = await vectorStore.search(question, {
        topK: intentInfo.intent === 'COMPARISON' ? 6 : 4,
        versionIds: eligibleVersionIds,
        allowedStatuses: statusFilter ? [statusFilter] : null
      });
    }

    // 5. Generate Grounded AI Answer with Citations & Evidence
    const answerResult = await generateGroundedAnswer(question, retrievedChunks, {
      intentInfo,
      conflictWarning,
      eligibleVersions
    });

    const latencyMs = Date.now() - startTime;

    res.json({
      success: true,
      query: question,
      intent: intentInfo.intent,
      latencyMs,
      eligibleVersionsCount: eligibleVersions.length,
      eligibleVersions: eligibleVersions.map(v => ({
        id: v.id,
        versionNumber: v.version_number,
        status: v.status,
        documentId: v.document_id,
        effectiveDate: v.effective_date
      })),
      result: {
        ...answerResult,
        statusNote
      }
    });
  } catch (err) {
    next(err);
  }
});

export default router;
