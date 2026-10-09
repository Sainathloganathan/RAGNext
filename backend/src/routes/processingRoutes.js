import express from 'express';
import { documentRepository } from '../repositories/documentRepository.js';

const router = express.Router();

/**
 * GET /api/processing/:jobId — Check background ingestion job progress
 */
router.get('/:jobId', async (req, res, next) => {
  try {
    const job = await documentRepository.getProcessingJob(req.params.jobId);
    if (!job) {
      return res.status(404).json({ success: false, error: 'Processing job not found' });
    }
    res.json({
      success: true,
      job
    });
  } catch (err) {
    next(err);
  }
});

export default router;
