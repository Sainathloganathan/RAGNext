import fs from 'fs';
import path from 'path';
import { config } from '../config/env.js';
import { generateEmbedding, cosineSimilarity } from '../embeddings/local_embedder.js';

let localVectors = [];

function loadLocalVectors() {
  const filePath = config.vectorStore.localVectorPath;
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  if (fs.existsSync(filePath)) {
    try {
      const data = fs.readFileSync(filePath, 'utf8');
      localVectors = JSON.parse(data);
    } catch (e) {
      localVectors = [];
    }
  }
}

function saveLocalVectors() {
  const filePath = config.vectorStore.localVectorPath;
  try {
    fs.writeFileSync(filePath, JSON.stringify(localVectors, null, 2), 'utf8');
  } catch (e) {
    console.error('❌ Failed to save vector storage:', e.message);
  }
}

// Initialize on module load
loadLocalVectors();

export const vectorStore = {
  /**
   * Index chunks into vector database with embeddings
   */
  async indexChunks(chunks) {
    if (!chunks || chunks.length === 0) return { indexed: 0 };

    // Remove existing chunks for this version to prevent duplicates
    const versionId = chunks[0].version_id;
    localVectors = localVectors.filter(v => v.metadata.version_id !== versionId);

    let indexedCount = 0;
    for (const chunk of chunks) {
      const embedding = await generateEmbedding(chunk.content);
      localVectors.push({
        id: chunk.id,
        embedding,
        content: chunk.content,
        metadata: {
          chunk_id: chunk.id,
          version_id: chunk.version_id,
          document_id: chunk.document_id,
          group_id: chunk.group_id,
          document_title: chunk.document_title,
          version_number: chunk.version_number,
          page_number: chunk.page_number,
          section_title: chunk.section_title,
          status: chunk.status,
          effective_date: chunk.effective_date,
          expiration_date: chunk.expiration_date
        }
      });
      indexedCount++;
    }

    saveLocalVectors();
    return { indexed: indexedCount };
  },

  /**
   * Search chunks by semantic similarity with metadata filters
   */
  async search(query, options = {}) {
    loadLocalVectors();
    const {
      topK = 5,
      versionIds = null,
      allowedStatuses = null,
      groupId = null,
      minScore = 0.1
    } = options;

    if (!query || !query.trim()) return [];

    const queryEmbedding = await generateEmbedding(query);
    const results = [];

    for (const item of localVectors) {
      // 1. Version filter
      if (versionIds && versionIds.length > 0) {
        if (!versionIds.includes(item.metadata.version_id)) {
          continue;
        }
      }

      // 2. Status filter
      if (allowedStatuses && allowedStatuses.length > 0) {
        if (!allowedStatuses.includes(item.metadata.status)) {
          continue;
        }
      }

      // 3. Group filter
      if (groupId) {
        if (item.metadata.group_id !== groupId) {
          continue;
        }
      }

      // Calculate semantic similarity score
      const score = cosineSimilarity(queryEmbedding, item.embedding);

      // Keyword boost for exact phrase hits
      let finalScore = score;
      const queryLower = query.toLowerCase();
      const contentLower = item.content.toLowerCase();
      const queryWords = queryLower.split(/\s+/).filter(w => w.length > 3);
      
      let matchedWords = 0;
      for (const w of queryWords) {
        if (contentLower.includes(w)) matchedWords++;
      }

      if (queryWords.length > 0) {
        const keywordRatio = matchedWords / queryWords.length;
        finalScore = (score * 0.7) + (keywordRatio * 0.3);
      }

      if (finalScore >= minScore) {
        results.push({
          id: item.id,
          content: item.content,
          metadata: item.metadata,
          score: Math.min(1.0, parseFloat(finalScore.toFixed(4)))
        });
      }
    }

    // Sort descending by score
    results.sort((a, b) => b.score - a.score);
    return results.slice(0, topK);
  },

  /**
   * Delete all chunks belonging to a version
   */
  async deleteByVersionId(versionId) {
    const beforeCount = localVectors.length;
    localVectors = localVectors.filter(v => v.metadata.version_id !== versionId);
    saveLocalVectors();
    return { deleted: beforeCount - localVectors.length };
  },

  /**
   * Delete all chunks for a document
   */
  async deleteByDocumentId(documentId) {
    const beforeCount = localVectors.length;
    localVectors = localVectors.filter(v => v.metadata.document_id !== documentId);
    saveLocalVectors();
    return { deleted: beforeCount - localVectors.length };
  },

  /**
   * Clear all vectors (for demo reset)
   */
  async resetAll() {
    localVectors = [];
    saveLocalVectors();
    return { success: true };
  }
};
