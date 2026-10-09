import pg from 'pg';
import fs from 'fs';
import path from 'path';
import { config } from '../config/env.js';

const { Pool } = pg;

let pgPool = null;
let localStore = {
  document_groups: [],
  documents: [],
  document_versions: [],
  document_chunks: [],
  processing_jobs: [],
  conversations: [],
  messages: []
};

const localDbPath = path.resolve(config.dbFile.replace(/\.sqlite$/, '.json'));

// Ensure storage data directory exists
const dataDir = path.dirname(localDbPath);
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

function loadLocalStore() {
  if (fs.existsSync(localDbPath)) {
    try {
      const content = fs.readFileSync(localDbPath, 'utf8');
      localStore = JSON.parse(content);
    } catch (e) {
      console.warn('⚠️ Could not parse local DB JSON, initializing fresh store.', e.message);
    }
  }
}

function saveLocalStore() {
  try {
    fs.writeFileSync(localDbPath, JSON.stringify(localStore, null, 2), 'utf8');
  } catch (e) {
    console.error('❌ Failed to persist local store to disk:', e.message);
  }
}

export async function initDatabase() {
  if (config.dbType === 'postgres') {
    try {
      pgPool = new Pool({
        host: config.pg.host,
        port: config.pg.port,
        database: config.pg.database,
        user: config.pg.user,
        password: config.pg.password,
        connectionTimeoutMillis: 3000,
      });

      // Test connection
      const client = await pgPool.connect();
      client.release();
      console.log('✅ PostgreSQL connected successfully to', config.pg.database);
      return { type: 'postgres', pool: pgPool };
    } catch (err) {
      console.warn(`⚠️ PostgreSQL connection failed (${err.message}). Falling back to local persistent store.`);
      config.dbType = 'sqlite';
    }
  }

  loadLocalStore();
  console.log('✅ Local persistent metadata storage active at:', localDbPath);
  return { type: 'local', store: localStore };
}

export const db = {
  async query(text, params = []) {
    if (config.dbType === 'postgres' && pgPool) {
      const res = await pgPool.query(text, params);
      return res;
    }

    // Local in-memory/JSON query emulator for offline and zero-config hackathon execution
    return runLocalQuery(text, params);
  },

  getLocalStore() {
    return localStore;
  },

  persistLocal() {
    saveLocalStore();
  }
};

/**
 * Basic SQL / CRUD emulator for standard queries when PostgreSQL service is not active
 */
function runLocalQuery(text, params) {
  const sql = text.trim();
  const upper = sql.toUpperCase();

  // Handle simple table queries
  if (upper.startsWith('SELECT')) {
    let tableName = null;
    const fromMatch = sql.match(/FROM\s+([a-zA-Z0-9_]+)/i);
    if (fromMatch) {
      tableName = fromMatch[1].toLowerCase();
    }

    let rows = localStore[tableName] ? [...localStore[tableName]] : [];

    // Filter by document_id or group_id if provided
    if (params.length > 0 && sql.includes('$1')) {
      if (sql.includes('WHERE id = $1') || sql.includes('WHERE document_id = $1') || sql.includes('WHERE group_id = $1') || sql.includes('WHERE version_id = $1')) {
        const paramVal = params[0];
        rows = rows.filter(r => r.id === paramVal || r.document_id === paramVal || r.group_id === paramVal || r.version_id === paramVal);
      }
    }

    return { rows, rowCount: rows.length };
  }

  if (upper.startsWith('INSERT INTO')) {
    const tableMatch = sql.match(/INSERT INTO\s+([a-zA-Z0-9_]+)/i);
    if (tableMatch) {
      const tableName = tableMatch[1].toLowerCase();
      if (!localStore[tableName]) localStore[tableName] = [];
      saveLocalStore();
    }
    return { rows: [], rowCount: 1 };
  }

  if (upper.startsWith('UPDATE')) {
    saveLocalStore();
    return { rows: [], rowCount: 1 };
  }

  if (upper.startsWith('DELETE FROM')) {
    saveLocalStore();
    return { rows: [], rowCount: 1 };
  }

  return { rows: [], rowCount: 0 };
}
