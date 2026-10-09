import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  FileText, 
  CheckCircle2, 
  Clock, 
  AlertCircle, 
  Upload, 
  MessageSquare, 
  ArrowRight,
  Database,
  Sparkles,
  RefreshCw
} from 'lucide-react';
import { api } from '../services/api';
import { StatusBadge, FormatBadge } from '../components/StatusBadge';

export function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [seeding, setSeeding] = useState(false);
  const [bannerMsg, setBannerMsg] = useState(null);

  const fetchStats = () => {
    setLoading(true);
    api.getDashboardStats()
      .then(res => {
        if (res.success) {
          setStats(res.stats);
        }
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const handleSeedDemo = async () => {
    setSeeding(true);
    setBannerMsg('Seeding Hackathon Leave Policy dataset (v1.0, v2.0, v3.0)...');
    try {
      const res = await api.seedDemoLeavePolicy();
      if (res.success) {
        setBannerMsg('✅ Successfully loaded 3 versions of Leave Policy. v3.0 is Active (20 days), v1.0 & v2.0 are Superseded.');
        fetchStats();
      }
    } catch (e) {
      setBannerMsg('❌ Failed to seed demo data.');
    } finally {
      setSeeding(false);
    }
  };

  return (
    <div className="container">
      
      {/* Top Banner / Welcome */}
      <div className="d-flex flex-wrap align-items-center justify-content-between mb-4 pb-3 border-bottom gap-3">
        <div>
          <h2 className="fw-bold mb-1">Document Intelligence Dashboard</h2>
          <p className="text-muted mb-0" style={{ fontSize: '0.9rem' }}>
            "Find the right information, from the right document version, with verifiable evidence."
          </p>
        </div>
        <div className="d-flex align-items-center gap-2">
          <button 
            className="btn btn-outline-success btn-sm d-flex align-items-center gap-1"
            onClick={handleSeedDemo}
            disabled={seeding}
            title="Ingests Leave Policy v1.0 (15d), v2.0 (18d), and v3.0 (20d)"
          >
            <Sparkles size={14} />
            <span>{seeding ? 'Loading Demo Data...' : 'Seed Demo Dataset'}</span>
          </button>
          <Link to="/upload" className="btn-green">
            <Upload size={16} />
            <span>Upload Document</span>
          </Link>
        </div>
      </div>

      {bannerMsg && (
        <div className="alert alert-success alert-dismissible fade show d-flex align-items-center justify-content-between mb-4" role="alert">
          <span style={{ fontSize: '0.9rem' }}>{bannerMsg}</span>
          <button type="button" className="btn-close" onClick={() => setBannerMsg(null)}></button>
        </div>
      )}

      {/* Real Stat Cards (4 metrics from backend) */}
      <div className="row g-3 mb-4">
        
        <div className="col-12 col-sm-6 col-lg-3">
          <div className="card-ragnext stat-card-widget">
            <div className="stat-icon-wrapper">
              <FileText size={24} />
            </div>
            <div>
              <div className="stat-number-val">{loading ? '-' : stats?.totalDocuments || 0}</div>
              <div className="stat-label-text">Total Documents</div>
            </div>
          </div>
        </div>

        <div className="col-12 col-sm-6 col-lg-3">
          <div className="card-ragnext stat-card-widget">
            <div className="stat-icon-wrapper" style={{ background: '#ECFDF5', color: '#059669' }}>
              <CheckCircle2 size={24} />
            </div>
            <div>
              <div className="stat-number-val text-success">{loading ? '-' : stats?.activeVersionsCount || 0}</div>
              <div className="stat-label-text">Active Versions</div>
            </div>
          </div>
        </div>

        <div className="col-12 col-sm-6 col-lg-3">
          <div className="card-ragnext stat-card-widget">
            <div className="stat-icon-wrapper" style={{ background: '#EFF6FF', color: '#2563EB' }}>
              <Database size={24} />
            </div>
            <div>
              <div className="stat-number-val text-primary">{loading ? '-' : stats?.totalVersionsCount || 0}</div>
              <div className="stat-label-text">Indexed Versions</div>
            </div>
          </div>
        </div>

        <div className="col-12 col-sm-6 col-lg-3">
          <div className="card-ragnext stat-card-widget">
            <div className="stat-icon-wrapper" style={{ background: '#FFFBEB', color: '#D97706' }}>
              <Clock size={24} />
            </div>
            <div>
              <div className="stat-number-val text-warning">{loading ? '-' : stats?.processingCount || 0}</div>
              <div className="stat-label-text">In Processing</div>
            </div>
          </div>
        </div>

      </div>

      {/* Main Grid: Recent Documents & AI Quick Start */}
      <div className="row g-4">
        
        {/* Recent Documents Table */}
        <div className="col-12 col-lg-8">
          <div className="card-ragnext">
            <div className="card-header-clean">
              <h5>Recent Documents</h5>
              <Link to="/documents" className="text-decoration-none text-success fw-bold d-flex align-items-center gap-1" style={{ fontSize: '0.84rem' }}>
                <span>View Library</span>
                <ArrowRight size={14} />
              </Link>
            </div>

            <div className="table-responsive">
              <table className="table table-hover align-middle mb-0" style={{ fontSize: '0.88rem' }}>
                <thead className="table-light text-muted" style={{ fontSize: '0.78rem', textTransform: 'uppercase' }}>
                  <tr>
                    <th>Document Title</th>
                    <th>Category</th>
                    <th>Active Version</th>
                    <th>Status</th>
                    <th className="text-end">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan="5" className="text-center py-4 text-muted">Loading documents from database...</td>
                    </tr>
                  ) : (!stats?.recentDocuments || stats.recentDocuments.length === 0) ? (
                    <tr>
                      <td colSpan="5" className="text-center py-4 text-muted">
                        No documents uploaded yet. Click <strong>"Seed Demo Dataset"</strong> or <strong>"Upload Document"</strong> to start.
                      </td>
                    </tr>
                  ) : (
                    stats.recentDocuments.map(doc => (
                      <tr key={doc.id}>
                        <td>
                          <div className="fw-bold text-dark">{doc.title}</div>
                          <small className="text-muted" style={{ fontSize: '0.72rem' }}>{doc.group_name || 'General'}</small>
                        </td>
                        <td><span className="badge bg-light text-dark border">{doc.category}</span></td>
                        <td><span className="fw-bold font-monospace text-primary">v{doc.active_version}</span></td>
                        <td><StatusBadge status={doc.latest_status} /></td>
                        <td className="text-end">
                          <Link to={`/documents/${doc.id}/versions`} className="btn btn-sm btn-outline-secondary me-1" title="View Version Lineage">
                            Versions ({doc.version_count})
                          </Link>
                          <Link to="/chat" className="btn btn-sm btn-success" title="Ask AI">
                            <MessageSquare size={13} />
                          </Link>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

          </div>
        </div>

        {/* AI Quick Chat CTA Card */}
        <div className="col-12 col-lg-4">
          <div className="card-ragnext p-4">
            <div className="d-flex align-items-center gap-2 mb-3 text-success">
              <Sparkles size={20} />
              <h5 className="mb-0 fw-bold">Ask Version-Aware AI</h5>
            </div>
            <p className="text-muted" style={{ fontSize: '0.86rem', lineHeight: '1.5' }}>
              Query all uploaded policies and manuals. The RAG engine verifies document versions, eliminates deprecated rules, and returns verifiable page citations.
            </p>

            <div className="d-flex flex-column gap-2 mb-3">
              <span className="text-muted" style={{ fontSize: '0.74rem', textTransform: 'uppercase', fontWeight: 'bold' }}>Sample Inquiries:</span>
              <Link to="/chat" className="query-chip text-decoration-none">
                "What is the current annual leave allowance?"
              </Link>
              <Link to="/chat" className="query-chip text-decoration-none">
                "What was the allowance in version 2?"
              </Link>
              <Link to="/chat" className="query-chip text-decoration-none">
                "Where does the document describe maternity leave?"
              </Link>
            </div>

            <Link to="/chat" className="btn-green w-100 justify-content-center">
              <MessageSquare size={16} />
              <span>Launch AI Document Chat</span>
            </Link>
          </div>
        </div>

      </div>

    </div>
  );
}
