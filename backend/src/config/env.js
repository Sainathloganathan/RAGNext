import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env from backend or root directory
dotenv.config({ path: path.resolve(__dirname, '../../.env') });
dotenv.config();

export const config = {
  port: parseInt(process.env.PORT || '5000', 10),
  nodeEnv: process.env.NODE_ENV || 'development',
  frontendUrl: process.env.FRONTEND_URL || 'http://localhost:5173',

  // Database
  dbType: process.env.DB_TYPE || 'sqlite', // 'postgres' | 'sqlite'
  dbFile: path.resolve(__dirname, '../../../', process.env.DB_FILE || './storage/data/ragnext.sqlite'),
  pg: {
    host: process.env.PG_HOST || 'localhost',
    port: parseInt(process.env.PG_PORT || '5432', 10),
    database: process.env.PG_DATABASE || 'ragnext_db',
    user: process.env.PG_USER || 'postgres',
    password: process.env.PG_PASSWORD || 'postgres',
  },

  // Ollama
  ollama: {
    baseUrl: process.env.OLLAMA_BASE_URL || 'http://localhost:11434',
    llmModel: process.env.OLLAMA_LLM_MODEL || 'llama3.2',
    embedModel: process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text',
  },

  // Vector Store
  vectorStore: {
    type: process.env.VECTOR_STORE_TYPE || 'embedded', // 'chroma' | 'embedded'
    chromaUrl: process.env.CHROMA_URL || 'http://localhost:8000',
    collectionName: process.env.CHROMA_COLLECTION || 'ragnext_documents',
    localVectorPath: path.resolve(__dirname, '../../../storage/vectors/vectors.json'),
  },

  // Storage and Chunks
  storageDir: path.resolve(__dirname, '../../../', process.env.STORAGE_DIR || './storage/uploads'),
  maxUploadSizeMb: parseInt(process.env.MAX_UPLOAD_SIZE_MB || '25', 10),
  chunkSize: parseInt(process.env.CHUNK_SIZE || '500', 10),
  chunkOverlap: parseInt(process.env.CHUNK_OVERLAP || '100', 10),
};
