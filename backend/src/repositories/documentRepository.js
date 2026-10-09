import { db } from '../database/db.js';
import { config } from '../config/env.js';

export const documentRepository = {
  // Document Groups
  async getAllGroups() {
    if (config.dbType === 'postgres') {
      const res = await db.query('SELECT * FROM document_groups ORDER BY created_at DESC');
      return res.rows;
    }
    return db.getLocalStore().document_groups;
  },

  async getGroupById(id) {
    if (config.dbType === 'postgres') {
      const res = await db.query('SELECT * FROM document_groups WHERE id = $1', [id]);
      return res.rows[0] || null;
    }
    return db.getLocalStore().document_groups.find(g => g.id === id) || null;
  },

  async createGroup(group) {
    if (config.dbType === 'postgres') {
      await db.query(
        'INSERT INTO document_groups (id, name, description, category, created_at, updated_at) VALUES ($1, $2, $3, $4, $5, $6)',
        [group.id, group.name, group.description, group.category, group.created_at, group.updated_at]
      );
      return group;
    }
    db.getLocalStore().document_groups.push(group);
    db.persistLocal();
    return group;
  },

  // Documents
  async getAllDocuments() {
    if (config.dbType === 'postgres') {
      const sql = `
        SELECT d.*, g.name as group_name,
          (SELECT COUNT(*) FROM document_versions v WHERE v.document_id = d.id) as version_count,
          (SELECT status FROM document_versions v WHERE v.document_id = d.id ORDER BY v.uploaded_at DESC LIMIT 1) as latest_status,
          (SELECT version_number FROM document_versions v WHERE v.document_id = d.id AND v.status = 'Active' LIMIT 1) as active_version
        FROM documents d
        LEFT JOIN document_groups g ON d.group_id = g.id
        ORDER BY d.created_at DESC
      `;
      const res = await db.query(sql);
      return res.rows;
    }

    const store = db.getLocalStore();
    return store.documents.map(d => {
      const group = store.document_groups.find(g => g.id === d.group_id);
      const versions = store.document_versions.filter(v => v.document_id === d.id);
      const activeVer = versions.find(v => v.status === 'Active');
      const latestVer = [...versions].sort((a, b) => new Date(b.uploaded_at) - new Date(a.uploaded_at))[0];

      return {
        ...d,
        group_name: group ? group.name : 'General',
        version_count: versions.length,
        latest_status: latestVer ? latestVer.status : 'Draft',
        active_version: activeVer ? activeVer.version_number : (latestVer ? latestVer.version_number : 'None'),
        processing_status: latestVer ? latestVer.processing_status : 'Completed'
      };
    });
  },

  async getDocumentById(id) {
    if (config.dbType === 'postgres') {
      const res = await db.query('SELECT * FROM documents WHERE id = $1', [id]);
      return res.rows[0] || null;
    }
    return db.getLocalStore().documents.find(d => d.id === id) || null;
  },

  async createDocument(doc) {
    if (config.dbType === 'postgres') {
      await db.query(
        'INSERT INTO documents (id, group_id, title, category, created_at) VALUES ($1, $2, $3, $4, $5)',
        [doc.id, doc.group_id, doc.title, doc.category, doc.created_at]
      );
      return doc;
    }
    db.getLocalStore().documents.push(doc);
    db.persistLocal();
    return doc;
  },

  async deleteDocument(id) {
    if (config.dbType === 'postgres') {
      await db.query('DELETE FROM documents WHERE id = $1', [id]);
      return true;
    }
    const store = db.getLocalStore();
    store.documents = store.documents.filter(d => d.id !== id);
    const verIds = store.document_versions.filter(v => v.document_id === id).map(v => v.id);
    store.document_versions = store.document_versions.filter(v => v.document_id !== id);
    store.document_chunks = store.document_chunks.filter(c => !verIds.includes(c.version_id));
    db.persistLocal();
    return true;
  },

  // Document Versions
  async getVersionsByDocumentId(documentId) {
    if (config.dbType === 'postgres') {
      const res = await db.query('SELECT * FROM document_versions WHERE document_id = $1 ORDER BY uploaded_at DESC', [documentId]);
      return res.rows;
    }
    return db.getLocalStore().document_versions
      .filter(v => v.document_id === documentId)
      .sort((a, b) => new Date(b.uploaded_at) - new Date(a.uploaded_at));
  },

  async getVersionsByGroupId(groupId) {
    if (config.dbType === 'postgres') {
      const res = await db.query('SELECT * FROM document_versions WHERE group_id = $1 ORDER BY uploaded_at DESC', [groupId]);
      return res.rows;
    }
    return db.getLocalStore().document_versions
      .filter(v => v.group_id === groupId)
      .sort((a, b) => new Date(b.uploaded_at) - new Date(a.uploaded_at));
  },

  async getVersionById(versionId) {
    if (config.dbType === 'postgres') {
      const res = await db.query('SELECT * FROM document_versions WHERE id = $1', [versionId]);
      return res.rows[0] || null;
    }
    return db.getLocalStore().document_versions.find(v => v.id === versionId) || null;
  },

  async createVersion(version) {
    if (config.dbType === 'postgres') {
      const sql = `
        INSERT INTO document_versions (
          id, document_id, group_id, version_number, status, file_name, file_path,
          file_size, mime_type, checksum, effective_date, expiration_date, description,
          uploaded_at, processing_status, error_message
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
      `;
      await db.query(sql, [
        version.id, version.document_id, version.group_id, version.version_number,
        version.status, version.file_name, version.file_path, version.file_size,
        version.mime_type, version.checksum, version.effective_date, version.expiration_date,
        version.description, version.uploaded_at, version.processing_status, version.error_message
      ]);
      return version;
    }
    db.getLocalStore().document_versions.push(version);
    db.persistLocal();
    return version;
  },

  async updateVersionStatus(versionId, status) {
    if (config.dbType === 'postgres') {
      await db.query('UPDATE document_versions SET status = $1 WHERE id = $2', [status, versionId]);
      return true;
    }
    const ver = db.getLocalStore().document_versions.find(v => v.id === versionId);
    if (ver) {
      ver.status = status;
      db.persistLocal();
    }
    return true;
  },

  async updateVersionProcessing(versionId, processingStatus, errorMessage = null) {
    if (config.dbType === 'postgres') {
      await db.query('UPDATE document_versions SET processing_status = $1, error_message = $2 WHERE id = $3', [processingStatus, errorMessage, versionId]);
      return true;
    }
    const ver = db.getLocalStore().document_versions.find(v => v.id === versionId);
    if (ver) {
      ver.processing_status = processingStatus;
      ver.error_message = errorMessage;
      db.persistLocal();
    }
    return true;
  },

  // Chunks
  async saveChunks(chunks) {
    if (!chunks || chunks.length === 0) return;
    if (config.dbType === 'postgres') {
      for (const c of chunks) {
        await db.query(
          'INSERT INTO document_chunks (id, version_id, chunk_index, page_number, section_title, content, token_count, created_at) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
          [c.id, c.version_id, c.chunk_index, c.page_number, c.section_title, c.content, c.token_count, c.created_at]
        );
      }
      return;
    }
    const store = db.getLocalStore();
    // Remove older chunks if reprocessing
    const verId = chunks[0].version_id;
    store.document_chunks = store.document_chunks.filter(c => c.version_id !== verId);
    store.document_chunks.push(...chunks);
    db.persistLocal();
  },

  async getChunksByVersionIds(versionIds) {
    if (!versionIds || versionIds.length === 0) return [];
    if (config.dbType === 'postgres') {
      const placeholders = versionIds.map((_, i) => `$${i + 1}`).join(',');
      const res = await db.query(`SELECT * FROM document_chunks WHERE version_id IN (${placeholders}) ORDER BY chunk_index ASC`, versionIds);
      return res.rows;
    }
    return db.getLocalStore().document_chunks.filter(c => versionIds.includes(c.version_id));
  },

  // Jobs
  async createProcessingJob(job) {
    if (config.dbType === 'postgres') {
      await db.query(
        'INSERT INTO processing_jobs (id, version_id, status, progress, step, error_message, created_at, updated_at) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
        [job.id, job.version_id, job.status, job.progress, job.step, job.error_message, job.created_at, job.updated_at]
      );
      return job;
    }
    db.getLocalStore().processing_jobs.push(job);
    db.persistLocal();
    return job;
  },

  async updateProcessingJob(jobId, updates) {
    if (config.dbType === 'postgres') {
      await db.query(
        'UPDATE processing_jobs SET status = $1, progress = $2, step = $3, error_message = $4, updated_at = $5 WHERE id = $6',
        [updates.status, updates.progress, updates.step, updates.error_message || null, new Date().toISOString(), jobId]
      );
      return true;
    }
    const job = db.getLocalStore().processing_jobs.find(j => j.id === jobId);
    if (job) {
      Object.assign(job, updates, { updated_at: new Date().toISOString() });
      db.persistLocal();
    }
    return true;
  },

  async getProcessingJob(jobId) {
    if (config.dbType === 'postgres') {
      const res = await db.query('SELECT * FROM processing_jobs WHERE id = $1', [jobId]);
      return res.rows[0] || null;
    }
    return db.getLocalStore().processing_jobs.find(j => j.id === jobId) || null;
  },

  // Dashboard Stats
  async getDashboardStats() {
    const docs = await this.getAllDocuments();
    const versions = config.dbType === 'postgres'
      ? (await db.query('SELECT * FROM document_versions')).rows
      : db.getLocalStore().document_versions;
    
    const activeVersions = versions.filter(v => v.status === 'Active');
    const processingVersions = versions.filter(v => v.processing_status !== 'Indexed' && v.processing_status !== 'Failed');

    const recentDocs = docs.slice(0, 5);
    const recentQueries = config.dbType === 'postgres'
      ? (await db.query('SELECT * FROM messages WHERE role = \'user\' ORDER BY created_at DESC LIMIT 5')).rows
      : db.getLocalStore().messages.filter(m => m.role === 'user').slice(-5).reverse();

    return {
      totalDocuments: docs.length,
      activeVersionsCount: activeVersions.length,
      processingCount: processingVersions.length,
      totalVersionsCount: versions.length,
      recentDocuments: recentDocs,
      recentQuestions: recentQueries
    };
  }
};
