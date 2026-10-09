import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  FileText, 
  Search, 
  Filter, 
  Trash2, 
  MessageSquare, 
  Plus, 
  Layers,
  Sparkles,
  ExternalLink
} from 'lucide-react';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';

export function DocumentsPage() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [categoryFilter, setCategoryFilter] = useState('ALL');
  const [actionMsg, setActionMsg] = useState(null);

  const fetchDocs = () => {
    setLoading(true);
    api.getDocuments()
      .then(res => {
        if (res.success) {
          setDocuments(res.documents || []);
        }
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleDelete = async (id, title) => {
    if (window.confirm(`Are you sure you want to delete "${title}" and all its indexed version chunks?`)) {
      try {
        const res = await api.deleteDocument(id);
        if (res.success) {
          setActionMsg(`Document "${title}" was deleted.`);
          fetchDocs();
        }
      } catch (e) {
        alert('Failed to delete document.');
      }
    }
  };

  const filteredDocs = documents.filter(doc => {
    const matchesSearch = doc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          (doc.category && doc.category.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesStatus = statusFilter === 'ALL' || doc.latest_status === statusFilter;
    const matchesCategory = categoryFilter === 'ALL' || doc.category === categoryFilter;
    return matchesSearch && matchesStatus && matchesCategory;
  });

  const uniqueCategories = Array.from(new Set(documents.map(d => d.category).filter(Boolean)));

  return (
    <div className="container">
      
      {/* Header Bar */}
      <div className="d-flex flex-wrap align-items-center justify-content-between mb-4 pb-3 border-bottom gap-3">
        <div>
          <h2 className="fw-bold mb-1">Document Library</h2>
          <p className="text-muted mb-0" style={{ fontSize: '0.9rem' }}>
            Manage, verify, and inspect multi-version documents indexed in RAGNext.
          </p>
        </div>
        <div className="d-flex gap-2">
          <Link to="/upload" className="btn-green">
            <Plus size={16} />
            <span>Upload New Document</span>
          </Link>
        </div>
      </div>

      {actionMsg && (
        <div className="alert alert-info alert-dismissible fade show mb-4" role="alert">
          <span>{actionMsg}</span>
          <button type="button" className="btn-close" onClick={() => setActionMsg(null)}></button>
        </div>
      )}

      {/* Filter and Search Toolbar */}
      <div className="card-ragnext p-3 mb-4">
        <div className="row g-2">
          
          <div className="col-12 col-md-6">
            <div className="input-group">
              <span className="input-group-text bg-white text-muted"><Search size={16} /></span>
              <input 
                type="text" 
                className="form-control" 
                placeholder="Search documents by title or keyword..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>

          <div className="col-6 col-md-3">
            <select 
              className="form-select"
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
            >
              <option value="ALL">All Categories</option>
              {uniqueCategories.map(c => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          <div className="col-6 col-md-3">
            <select 
              className="form-select"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="ALL">All Statuses</option>
              <option value="Active">Active</option>
              <option value="Superseded">Superseded</option>
              <option value="Draft">Draft</option>
              <option value="Archived">Archived</option>
            </select>
          </div>

        </div>
      </div>

      {/* Documents Table */}
      <div className="card-ragnext">
        <div className="table-responsive">
          <table className="table table-hover align-middle mb-0" style={{ fontSize: '0.88rem' }}>
            <thead className="table-light text-muted" style={{ fontSize: '0.78rem', textTransform: 'uppercase' }}>
              <tr>
                <th>Document Title</th>
                <th>Category</th>
                <th>Active Version</th>
                <th>Total Revisions</th>
                <th>Status</th>
                <th>Created Date</th>
                <th className="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="7" className="text-center py-5 text-muted">Loading documents...</td>
                </tr>
              ) : filteredDocs.length === 0 ? (
                <tr>
                  <td colSpan="7" className="text-center py-5 text-muted">
                    No documents match your query. Try adjusting your search filters or upload a document.
                  </td>
                </tr>
              ) : (
                filteredDocs.map(doc => (
                  <tr key={doc.id}>
                    <td>
                      <div className="fw-bold text-dark">{doc.title}</div>
                      <small className="text-muted" style={{ fontSize: '0.72rem' }}>ID: {doc.id}</small>
                    </td>
                    <td>
                      <span className="badge bg-light text-dark border">{doc.category || 'General'}</span>
                    </td>
                    <td>
                      <span className="fw-bold font-monospace text-success">
                        {doc.active_version !== 'None' ? `v${doc.active_version}` : 'None'}
                      </span>
                    </td>
                    <td>
                      <Link to={`/documents/${doc.id}/versions`} className="badge bg-secondary text-decoration-none">
                        {doc.version_count || 1} Revisions
                      </Link>
                    </td>
                    <td><StatusBadge status={doc.latest_status} /></td>
                    <td className="text-muted" style={{ fontSize: '0.8rem' }}>
                      {new Date(doc.created_at).toLocaleDateString()}
                    </td>
                    <td className="text-end">
                      <div className="d-flex justify-content-end gap-1">
                        <Link 
                          to={`/documents/${doc.id}/versions`} 
                          className="btn btn-sm btn-outline-primary d-inline-flex align-items-center gap-1"
                          title="View Version History & Lineage"
                        >
                          <Layers size={13} />
                          <span>Versions</span>
                        </Link>
                        <Link 
                          to="/chat" 
                          className="btn btn-sm btn-outline-success"
                          title="Ask AI about this document"
                        >
                          <MessageSquare size={13} />
                        </Link>
                        <button 
                          className="btn btn-sm btn-outline-danger"
                          onClick={() => handleDelete(doc.id, doc.title)}
                          title="Delete Document"
                        >
                          <Trash2 size={13} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
