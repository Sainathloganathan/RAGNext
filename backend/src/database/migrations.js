import { db } from './db.js';
import { config } from '../config/env.js';

export async function runMigrations() {
  if (config.dbType === 'postgres') {
    console.log('🔄 Running PostgreSQL database migrations...');
    const schemaSql = `
      CREATE TABLE IF NOT EXISTS document_groups (
        id VARCHAR(64) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        category VARCHAR(100) DEFAULT 'General',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS documents (
        id VARCHAR(64) PRIMARY KEY,
        group_id VARCHAR(64) REFERENCES document_groups(id) ON DELETE CASCADE,
        title VARCHAR(255) NOT NULL,
        category VARCHAR(100) DEFAULT 'General',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS document_versions (
        id VARCHAR(64) PRIMARY KEY,
        document_id VARCHAR(64) REFERENCES documents(id) ON DELETE CASCADE,
        group_id VARCHAR(64) REFERENCES document_groups(id) ON DELETE CASCADE,
        version_number VARCHAR(50) NOT NULL,
        status VARCHAR(50) NOT NULL DEFAULT 'Draft', -- Draft, Active, Superseded, Expired, Archived
        file_name VARCHAR(255) NOT NULL,
        file_path TEXT NOT NULL,
        file_size BIGINT NOT NULL,
        mime_type VARCHAR(100) NOT NULL,
        checksum VARCHAR(128),
        effective_date DATE,
        expiration_date DATE,
        description TEXT,
        uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        processing_status VARCHAR(50) DEFAULT 'Uploaded',
        error_message TEXT
      );

      CREATE TABLE IF NOT EXISTS document_chunks (
        id VARCHAR(128) PRIMARY KEY,
        version_id VARCHAR(64) REFERENCES document_versions(id) ON DELETE CASCADE,
        chunk_index INT NOT NULL,
        page_number INT DEFAULT 1,
        section_title VARCHAR(255),
        content TEXT NOT NULL,
        token_count INT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS processing_jobs (
        id VARCHAR(64) PRIMARY KEY,
        version_id VARCHAR(64) REFERENCES document_versions(id) ON DELETE CASCADE,
        status VARCHAR(50) DEFAULT 'Pending',
        progress INT DEFAULT 0,
        step VARCHAR(100),
        error_message TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS conversations (
        id VARCHAR(64) PRIMARY KEY,
        title VARCHAR(255) DEFAULT 'New Conversation',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS messages (
        id VARCHAR(64) PRIMARY KEY,
        conversation_id VARCHAR(64) REFERENCES conversations(id) ON DELETE CASCADE,
        role VARCHAR(20) NOT NULL, -- user, assistant, system
        content TEXT NOT NULL,
        sources JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );

      CREATE INDEX IF NOT EXISTS idx_doc_versions_group ON document_versions(group_id);
      CREATE INDEX IF NOT EXISTS idx_doc_versions_status ON document_versions(status);
      CREATE INDEX IF NOT EXISTS idx_chunks_version ON document_chunks(version_id);
    `;

    try {
      await db.query(schemaSql);
      console.log('✅ PostgreSQL migrations completed successfully.');
    } catch (err) {
      console.error('❌ Migration error:', err.message);
    }
  } else {
    console.log('✅ Local store schema ready (document_groups, documents, document_versions, chunks, jobs, conversations).');
  }
}
