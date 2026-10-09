import React, { useEffect, useState } from 'react';
import { 
  Settings, 
  Cpu, 
  Database, 
  HardDrive, 
  CheckCircle, 
  XCircle, 
  RefreshCw,
  Trash2,
  Shield,
  Layers
} from 'lucide-react';
import { api } from '../services/api';

export function SettingsPage() {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [resetting, setResetting] = useState(false);
  const [msg, setMsg] = useState(null);

  const fetchSettings = () => {
    setLoading(true);
    api.getSettingsStatus()
      .then(res => {
        if (res.success) setSettings(res.services);
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchSettings();
  }, []);

  const handleResetData = async () => {
    if (window.confirm('Are you sure you want to reset all demo documents and vector indexes?')) {
      setResetting(true);
      try {
        const res = await api.resetDemoData();
        if (res.success) {
          setMsg('Repository and vector storage successfully reset.');
        }
      } catch (e) {
        setMsg('Failed to reset repository.');
      } finally {
        setResetting(false);
      }
    }
  };

  return (
    <div className="container" style={{ maxWidth: '840px' }}>
      
      <div className="d-flex flex-wrap align-items-center justify-content-between mb-4 pb-3 border-bottom gap-3">
        <div>
          <h2 className="fw-bold mb-1">System & AI Engine Settings</h2>
          <p className="text-muted mb-0" style={{ fontSize: '0.88rem' }}>
            Live status of local AI inference, vector database, metadata storage, and offline capabilities.
          </p>
        </div>
        <button className="btn btn-outline-secondary btn-sm d-flex align-items-center gap-1" onClick={fetchSettings}>
          <RefreshCw size={14} />
          <span>Refresh Status</span>
        </button>
      </div>

      {msg && (
        <div className="alert alert-info alert-dismissible fade show mb-4" role="alert">
          <span>{msg}</span>
          <button type="button" className="btn-close" onClick={() => setMsg(null)}></button>
        </div>
      )}

      {/* Services Status Cards */}
      <div className="row g-3 mb-4">
        
        {/* 1. Ollama LLM & Embeddings */}
        <div className="col-12">
          <div className="card-ragnext p-4">
            <div className="d-flex align-items-center justify-content-between mb-3">
              <div className="d-flex align-items-center gap-2">
                <Cpu size={22} className="text-primary" />
                <h5 className="mb-0 fw-bold">Local AI Inference (Ollama)</h5>
              </div>
              <span className={`badge ${settings?.ollama?.connected ? 'bg-success' : 'bg-secondary'}`}>
                {settings?.ollama?.connected ? '● Connected' : '○ Standby / Fallback'}
              </span>
            </div>

            <p className="text-muted mb-3" style={{ fontSize: '0.86rem' }}>
              {settings?.ollama?.note}
            </p>

            <div className="row g-2 font-monospace" style={{ fontSize: '0.8rem' }}>
              <div className="col-12 col-md-6 bg-light p-2 rounded border">
                <strong>Ollama Endpoint:</strong> {settings?.ollama?.url || 'http://localhost:11434'}
              </div>
              <div className="col-12 col-md-6 bg-light p-2 rounded border">
                <strong>Configured LLM Model:</strong> {settings?.ollama?.selectedLlmModel || 'llama3.2'}
              </div>
              <div className="col-12 col-md-6 bg-light p-2 rounded border">
                <strong>Configured Embed Model:</strong> {settings?.ollama?.selectedEmbedModel || 'nomic-embed-text'}
              </div>
              <div className="col-12 col-md-6 bg-light p-2 rounded border">
                <strong>Available Local Models:</strong> {settings?.ollama?.availableModels?.length > 0 ? settings.ollama.availableModels.join(', ') : 'None detected'}
              </div>
            </div>

            {!settings?.ollama?.connected && (
              <div className="mt-3 alert alert-light border mb-0" style={{ fontSize: '0.82rem' }}>
                💡 <em>To enable Ollama inference:</em> Run <code>ollama run llama3.2</code> in your terminal. The RAGNext engine automatically connects when Ollama is running.
              </div>
            )}
          </div>
        </div>

        {/* 2. Metadata Database */}
        <div className="col-12 col-md-6">
          <div className="card-ragnext p-4 h-100">
            <div className="d-flex align-items-center justify-content-between mb-3">
              <div className="d-flex align-items-center gap-2">
                <Database size={20} className="text-success" />
                <h5 className="mb-0 fw-bold">Metadata Database</h5>
              </div>
              <span className="badge bg-success">● Connected</span>
            </div>

            <p className="text-muted mb-2" style={{ fontSize: '0.84rem' }}>
              Stores users, document families, version records, temporal timestamps, and processing job queues.
            </p>
            <div className="font-monospace bg-light p-2 rounded border" style={{ fontSize: '0.78rem' }}>
              <div><strong>Type:</strong> {settings?.metadataDatabase?.type?.toUpperCase()}</div>
              <div><strong>Location:</strong> {settings?.metadataDatabase?.location}</div>
            </div>
          </div>
        </div>

        {/* 3. Vector Database */}
        <div className="col-12 col-md-6">
          <div className="card-ragnext p-4 h-100">
            <div className="d-flex align-items-center justify-content-between mb-3">
              <div className="d-flex align-items-center gap-2">
                <Layers size={20} className="text-primary" />
                <h5 className="mb-0 fw-bold">Vector Storage</h5>
              </div>
              <span className="badge bg-success">● Active</span>
            </div>

            <p className="text-muted mb-2" style={{ fontSize: '0.84rem' }}>
              Stores semantic embeddings and chunk-level metadata (version ID, page number, section headers).
            </p>
            <div className="font-monospace bg-light p-2 rounded border" style={{ fontSize: '0.78rem' }}>
              <div><strong>Engine:</strong> {settings?.vectorStore?.type?.toUpperCase()}</div>
              <div><strong>Vector Path:</strong> storage/vectors/vectors.json</div>
            </div>
          </div>
        </div>

      </div>

      {/* Demo Reset Card */}
      <div className="card-ragnext p-4 border-danger border-opacity-25 mb-4">
        <div className="d-flex align-items-center justify-content-between">
          <div>
            <h6 className="fw-bold text-danger mb-1">Reset Repository Data</h6>
            <p className="text-muted mb-0" style={{ fontSize: '0.82rem' }}>
              Purges all uploaded documents, chunks, and vector embeddings for a fresh hackathon demonstration.
            </p>
          </div>
          <button 
            className="btn btn-outline-danger btn-sm d-flex align-items-center gap-1"
            onClick={handleResetData}
            disabled={resetting}
          >
            <Trash2 size={14} />
            <span>{resetting ? 'Resetting...' : 'Reset All Data'}</span>
          </button>
        </div>
      </div>

    </div>
  );
}
