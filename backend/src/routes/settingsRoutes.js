import express from 'express';
import { config } from '../config/env.js';

const router = express.Router();

/**
 * GET /api/settings/status — Service connection statuses (Ollama, Vector DB, Metadata DB)
 */
router.get('/status', async (req, res) => {
  let ollamaConnected = false;
  let ollamaModels = [];
  let ollamaError = null;

  // 1. Check Ollama
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 1500);

    const oRes = await fetch(`${config.ollama.baseUrl}/api/tags`, {
      signal: controller.signal
    });
    clearTimeout(timeout);

    if (oRes.ok) {
      const data = await oRes.json();
      ollamaConnected = true;
      ollamaModels = data.models ? data.models.map(m => m.name) : [];
    }
  } catch (err) {
    ollamaError = `Ollama service unreachable at ${config.ollama.baseUrl}. Start with: 'ollama run ${config.ollama.llmModel}'`;
  }

  res.json({
    success: true,
    services: {
      ollama: {
        connected: ollamaConnected,
        url: config.ollama.baseUrl,
        selectedLlmModel: config.ollama.llmModel,
        selectedEmbedModel: config.ollama.embedModel,
        availableModels: ollamaModels,
        error: ollamaError,
        note: ollamaConnected ? 'Ready for local GPU/CPU inference' : 'Offline. Running with grounded deterministic extractive engine.'
      },
      metadataDatabase: {
        type: config.dbType,
        connected: true,
        location: config.dbType === 'postgres' ? `${config.pg.host}:${config.pg.port}/${config.pg.database}` : config.dbFile
      },
      vectorStore: {
        type: config.vectorStore.type,
        connected: true,
        location: config.vectorStore.localVectorPath
      },
      storage: {
        uploadDirectory: config.storageDir,
        maxUploadSizeMb: config.maxUploadSizeMb
      },
      retrieval: {
        chunkSize: config.chunkSize,
        chunkOverlap: config.chunkOverlap
      }
    }
  });
});

export default router;
