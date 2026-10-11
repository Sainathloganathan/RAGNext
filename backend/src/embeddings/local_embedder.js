import { config } from '../config/env.js';

/**
 * Generates embeddings via local Ollama instance or deterministic fallback vectorizer
 */
export async function generateEmbedding(text) {
  if (!text || !text.trim()) {
    return new Array(64).fill(0);
  }

  // 1. Try local Ollama embedding API
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);

    const res = await fetch(`${config.ollama.baseUrl}/api/embeddings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: config.ollama.embedModel,
        prompt: text
      }),
      signal: controller.signal
    });

    clearTimeout(timeout);

    if (res.ok) {
      const data = await res.json();
      if (data.embedding && Array.isArray(data.embedding)) {
        return data.embedding;
      }
    }
  } catch (err) {
    // Ollama not running or timeout -> Fall back to deterministic local semantic vector
  }

  // 2. Deterministic local embedding fallback (TF-IDF / Character N-Gram hashing)
  return generateDeterministicVector(text);
}

/**
 * 128-dimensional deterministic dense vector based on semantic token frequencies and character hashing
 */
function generateDeterministicVector(text) {
  const DIM = 128;
  const vector = new Array(DIM).fill(0);
  const clean = text.toLowerCase().replace(/[^a-z0-9\s]/g, ' ');
  const words = clean.split(/\s+/).filter(w => w.length > 0);

  if (words.length === 0) return vector;

  for (let i = 0; i < words.length; i++) {
    const word = words[i];
    let hash = 0;
    for (let c = 0; c < word.length; c++) {
      hash = ((hash << 5) - hash) + word.charCodeAt(c);
      hash |= 0;
    }
    const idx = Math.abs(hash) % DIM;
    vector[idx] += 1.0;

    // Subword n-grams for typo & morphological matching
    if (word.length >= 4) {
      for (let g = 0; g < word.length - 3; g++) {
        const trigram = word.substring(g, g + 3);
        let gHash = 0;
        for (let tc = 0; tc < trigram.length; tc++) {
          gHash = ((gHash << 3) - gHash) + trigram.charCodeAt(tc);
          gHash |= 0;
        }
        const gIdx = Math.abs(gHash) % DIM;
        vector[gIdx] += 0.3;
      }
    }
  }

  // L2 Normalize
  let norm = 0;
  for (let i = 0; i < DIM; i++) norm += vector[i] * vector[i];
  norm = Math.sqrt(norm);

  if (norm > 0) {
    for (let i = 0; i < DIM; i++) vector[i] = vector[i] / norm;
  }

  return vector;
}

/**
 * Cosine similarity between two vectors
 */
export function cosineSimilarity(vecA, vecB) {
  if (!vecA || !vecB || vecA.length !== vecB.length) return 0;
  let dot = 0;
  let normA = 0;
  let normB = 0;

  for (let i = 0; i < vecA.length; i++) {
    dot += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }

  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}
