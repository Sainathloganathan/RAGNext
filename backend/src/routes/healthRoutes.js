import express from 'express';
import { config } from '../config/env.js';

const router = express.Router();

router.get('/', (req, res) => {
  res.json({
    status: 'healthy',
    product: 'RAGNext — Version-Aware Document Intelligence',
    team: 'Cyber Knights',
    problemStatement: 'SH-SVA-04',
    timestamp: new Date().toISOString(),
    environment: config.nodeEnv,
    database: config.dbType,
    vectorStore: config.vectorStore.type
  });
});

export default router;
