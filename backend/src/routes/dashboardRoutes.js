import express from 'express';
import { documentRepository } from '../repositories/documentRepository.js';

const router = express.Router();

router.get('/stats', async (req, res, next) => {
  try {
    const stats = await documentRepository.getDashboardStats();
    res.json({
      success: true,
      stats
    });
  } catch (err) {
    next(err);
  }
});

export default router;
