import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  Layers, 
  ArrowLeft, 
  CheckCircle, 
  Clock, 
  AlertTriangle, 
  FileText, 
  MessageSquare,
  Plus,
  ShieldCheck
} from 'lucide-react';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';

export function VersionHistoryPage() {
  const { id } = useParams();
  const [document, setDocument] = useState(null);
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionMsg, setActionMsg] = useState(null);
  const [updatingId, setUpdatingId] = useState(null);

  const fetchDocumentVersions = () => {
    setLoading(true);
    api.getDocument(id)
      .then(res => {
        if (res.success) {
          setDocument(res.document);
          setVersions(res.versions || []);
        }
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchDocumentVersions();
  }, [id]);

  const handleStatusChange = async (versionId, newStatus, supersedeOthers = false) => {
    setUpdatingId(versionId);
    try {
      const res = await api.updateVersionStatus(versionId, newStatus, supersedeOthers);
      if (res.success) {
        setActionMsg(res.message);
        fetchDocumentVersions();
      }
    } catch (e) {
      alert('Failed to update status.');
    } finally {
      setUpdatingId(null);
    }
  };

  const activeVersions = versions.filter(v => v.status === 'Active');
  const hasConflict = activeVersions.length > 1;

  return (
    <div className="container">
      
      {/* Back Button and Header */}
      <div className="d-flex align-items-center gap-2 mb-3">
        <Link to="/documents" className="text-decoration-none text-muted d-flex align-items-center gap-1" style={{ fontSize: '0.85rem' }}>
          <ArrowLeft size={16} />
          <span>Back to Document Library</span>
        </Link>
      </div>

      <div className="d-flex flex-wrap align-items-center justify-content-between mb-4 pb-3 border-bottom gap-3">
        <div>
          <div className="d-flex align-items-center gap-2 mb-1">
            <h2 className="fw-bold mb-0">{document ? document.title : 'Version History'}</h2>
            <span className="badge bg-light text-dark border">{document?.category}</span>
          </div>
          <p className="text-muted mb-0" style={{ fontSize: '0.88rem' }}>
            Lineage tracking, temporal validation, and status lifecycle management.
          </p>
        </div>
        <div className="d-flex gap-2">
          <Link to="/upload" className="btn btn-outline-success btn-sm d-flex align-items-center gap-1">
            <Plus size={14} />
            <span>Upload New Revision</span>
          </Link>
          <Link to="/chat" className="btn-green btn-sm">
            <MessageSquare size={14} />
            <span>Query this Document</span>
          </Link>
        </div>
      </div>

      {actionMsg && (
        <div className="alert alert-success alert-dismissible fade show mb-4" role="alert">
          <span>{actionMsg}</span>
          <button type="button" className="btn-close" onClick={() => setActionMsg(null)}></button>
        </div>
      )}

      {/* Conflict Warning Banner if multiple active versions exist */}
      {hasConflict && (
        <div className="alert alert-warning border-warning d-flex align-items-start gap-2 mb-4" role="alert">
          <AlertTriangle size={20} className="text-warning flex-shrink-0 mt-1" />
          <div>
            <strong>Administrative Conflict Detected:</strong> Multiple versions ({activeVersions.map(v => 'v' + v.version_number).join(', ')}) are currently marked <strong>Active</strong>. 
            The version-aware RAG engine will explicitly warn users of conflicting policies rather than silently guessing.
          </div>
        </div>
      )}

      {/* Version History Table */}
      <div className="card-ragnext mb-4">
        <div className="card-header-clean">
          <h5>Version Lineage & Temporal Status</h5>
          <span className="badge bg-secondary font-monospace">{versions.length} Revisions Recorded</span>
        </div>

        <div className="table-responsive">
          <table className="table table-hover align-middle mb-0" style={{ fontSize: '0.88rem' }}>
            <thead className="table-light text-muted" style={{ fontSize: '0.78rem', textTransform: 'uppercase' }}>
              <tr>
                <th>Version</th>
                <th>Status</th>
                <th>Uploaded File</th>
                <th>Effective Period</th>
                <th>Processing Status</th>
                <th>Notes / Description</th>
                <th className="text-end">Lifecycle Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="7" className="text-center py-4 text-muted">Loading version history...</td>
                </tr>
              ) : versions.length === 0 ? (
                <tr>
                  <td colSpan="7" className="text-center py-4 text-muted">No versions found for this document.</td>
                </tr>
              ) : (
                versions.map(v => (
                  <tr key={v.id} className={v.status === 'Active' ? 'table-success bg-opacity-10' : ''}>
                    <td>
                      <span className="fw-bold font-monospace text-primary" style={{ fontSize: '0.95rem' }}>
                        v{v.version_number}
                      </span>
                    </td>
                    <td>
                      <StatusBadge status={v.status} />
                    </td>
                    <td>
                      <div className="fw-semibold text-dark">{v.file_name}</div>
                      <small className="text-muted" style={{ fontSize: '0.72rem' }}>{(v.file_size / 1024).toFixed(1)} KB · {new Date(v.uploaded_at).toLocaleDateString()}</small>
                    </td>
                    <td>
                      <div style={{ fontSize: '0.8rem' }}>
                        <div><strong>From:</strong> {v.effective_date || 'Immediate'}</div>
                        {v.expiration_date && <div><strong>Until:</strong> {v.expiration_date}</div>}
                      </div>
                    </td>
                    <td>
                      <span className={`badge ${v.processing_status === 'Indexed' ? 'bg-success' : 'bg-warning text-dark'}`}>
                        {v.processing_status}
                      </span>
                    </td>
                    <td style={{ maxWidth: '200px' }}>
                      <span className="text-muted" style={{ fontSize: '0.78rem' }}>
                        {v.description || 'Standard revision upload.'}
                      </span>
                    </td>
                    <td className="text-end">
                      <div className="btn-group btn-group-sm">
                        {v.status !== 'Active' && (
                          <button 
                            className="btn btn-outline-success"
                            disabled={updatingId === v.id}
                            onClick={() => handleStatusChange(v.id, 'Active', true)}
                            title="Mark as Current Active Truth (supersedes other active versions)"
                          >
                            Set Active
                          </button>
                        )}
                        {v.status !== 'Superseded' && (
                          <button 
                            className="btn btn-outline-secondary"
                            disabled={updatingId === v.id}
                            onClick={() => handleStatusChange(v.id, 'Superseded')}
                            title="Mark as Superseded historical version"
                          >
                            Supersede
                          </button>
                        )}
                        {v.status !== 'Archived' && (
                          <button 
                            className="btn btn-outline-dark"
                            disabled={updatingId === v.id}
                            onClick={() => handleStatusChange(v.id, 'Archived')}
                            title="Archive version"
                          >
                            Archive
                          </button>
                        )}
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
