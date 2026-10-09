const API_BASE = '/api';

export const api = {
  async getHealth() {
    const res = await fetch(`${API_BASE}/health`);
    return res.json();
  },

  async getDashboardStats() {
    const res = await fetch(`${API_BASE}/dashboard/stats`);
    return res.json();
  },

  async getDocuments() {
    const res = await fetch(`${API_BASE}/documents`);
    return res.json();
  },

  async getDocument(id) {
    const res = await fetch(`${API_BASE}/documents/${id}`);
    return res.json();
  },

  async uploadDocument(formData) {
    const res = await fetch(`${API_BASE}/documents/upload`, {
      method: 'POST',
      body: formData
    });
    return res.json();
  },

  async deleteDocument(id) {
    const res = await fetch(`${API_BASE}/documents/${id}`, {
      method: 'DELETE'
    });
    return res.json();
  },

  async getDocumentVersions(docId) {
    const res = await fetch(`${API_BASE}/documents/${docId}/versions`);
    return res.json();
  },

  async updateVersionStatus(versionId, status, supersedePrevious = false) {
    const res = await fetch(`${API_BASE}/versions/${versionId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status, supersedePrevious })
    });
    return res.json();
  },

  async getProcessingJob(jobId) {
    const res = await fetch(`${API_BASE}/processing/${jobId}`);
    return res.json();
  },

  async sendChatMessage(payload) {
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async getSettingsStatus() {
    const res = await fetch(`${API_BASE}/settings/status`);
    return res.json();
  },

  async seedDemoLeavePolicy() {
    const res = await fetch(`${API_BASE}/demo/seed-leave-policy`, {
      method: 'POST'
    });
    return res.json();
  },

  async resetDemoData() {
    const res = await fetch(`${API_BASE}/demo/reset`, {
      method: 'POST'
    });
    return res.json();
  }
};
