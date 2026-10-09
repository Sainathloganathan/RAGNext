import express from 'express';
import { documentRepository } from '../repositories/documentRepository.js';
import { vectorStore } from '../retrieval/vector_store.js';

const router = express.Router();

/**
 * GET /api/documents/:documentId/versions — List all versions for a document
 */
router.get('/documents/:documentId/versions', async (req, res, next) => {
  try {
    const versions = await documentRepository.getVersionsByDocumentId(req.params.documentId);
    res.json({
      success: true,
      versions
    });
  } catch (err) {
    next(err);
  }
});

/**
 * PATCH /api/versions/:versionId/status — Change status (Active, Superseded, Expired, Archived, Draft)
 */
router.patch('/versions/:versionId/status', async (req, res, next) => {
  try {
    const { status } = req.body;
    const allowed = ['Draft', 'Active', 'Superseded', 'Expired', 'Archived'];

    if (!allowed.includes(status)) {
      return res.status(400).json({
        success: false,
        error: `Invalid status. Allowed values: ${allowed.join(', ')}`
      });
    }

    const version = await documentRepository.getVersionById(req.params.versionId);
    if (!version) {
      return res.status(404).json({ success: false, error: 'Version not found' });
    }

    await documentRepository.updateVersionStatus(version.id, status);

    // If marked active, optionally mark other versions in group as superseded if requested
    if (status === 'Active' && req.body.supersedePrevious) {
      const allGroupVersions = await documentRepository.getVersionsByGroupId(version.group_id);
      for (const v of allGroupVersions) {
        if (v.id !== version.id && v.status === 'Active') {
          await documentRepository.updateVersionStatus(v.id, 'Superseded');
        }
      }
    }

    res.json({
      success: true,
      message: `Version v${version.version_number} status updated to ${status}.`,
      versionId: version.id,
      newStatus: status
    });
  } catch (err) {
    next(err);
  }
});

export default router;
