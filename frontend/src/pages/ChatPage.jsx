import React, { useState, useEffect } from 'react';
import { 
  MessageSquare, 
  Send, 
  Sparkles, 
  AlertTriangle, 
  FileText, 
  Layers, 
  CheckCircle2, 
  Clock, 
  Info,
  ChevronDown,
  Trash2
} from 'lucide-react';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';

export function ChatPage() {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [selectedDocId, setSelectedDocId] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    api.getDocuments()
      .then(res => {
        if (res.success) setDocuments(res.documents || []);
      })
      .catch(() => {});
  }, []);

  const handleSend = async (queryToSend = null) => {
    const q = queryToSend || question;
    if (!q || !q.trim()) return;

    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: q,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMsg]);
    setQuestion('');
    setLoading(true);

    try {
      const res = await api.sendChatMessage({
        question: q,
        documentId: selectedDocId || null,
        statusFilter: statusFilter || null
      });

      if (res.success) {
        const botMsg = {
          id: Date.now() + 1,
          role: 'assistant',
          content: res.result.answer,
          evidenceStatus: res.result.evidenceStatus,
          confidenceScore: res.result.confidenceScore,
          sources: res.result.sources || [],
          conflictWarning: res.result.conflictWarning,
          missingInfoWarning: res.result.missingInfoWarning,
          engine: res.result.engine,
          intent: res.intent,
          latencyMs: res.latencyMs,
          eligibleVersions: res.eligibleVersions || [],
          timestamp: new Date().toLocaleTimeString()
        };
        setMessages(prev => [...prev, botMsg]);
      } else {
        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          role: 'assistant',
          content: `Error: ${res.error || 'Failed to generate answer.'}`,
          evidenceStatus: 'Error',
          timestamp: new Date().toLocaleTimeString()
        }]);
      }
    } catch (e) {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        content: `Network error: Could not reach backend RAG engine.`,
        evidenceStatus: 'Error',
        timestamp: new Date().toLocaleTimeString()
      }]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const runPreset = (text) => {
    setQuestion(text);
    handleSend(text);
  };

  return (
    <div className="container" style={{ maxWidth: '980px' }}>
      
      {/* Header and Scope Selector */}
      <div className="d-flex flex-wrap align-items-center justify-content-between mb-4 pb-3 border-bottom gap-3">
        <div>
          <h2 className="fw-bold mb-1">AI Document Intelligence Chat</h2>
          <p className="text-muted mb-0" style={{ fontSize: '0.88rem' }}>
            Version-aware question answering with verifiable page-level evidence citations.
          </p>
        </div>
        <div className="d-flex align-items-center gap-2">
          {messages.length > 0 && (
            <button className="btn btn-outline-secondary btn-sm d-flex align-items-center gap-1" onClick={clearChat}>
              <Trash2 size={14} />
              <span>Clear Chat</span>
            </button>
          )}
        </div>
      </div>

      {/* Scope and Retrieval Filters Bar */}
      <div className="card-ragnext p-3 mb-4 bg-light">
        <div className="row g-2 align-items-center">
          
          <div className="col-12 col-md-6">
            <div className="d-flex align-items-center gap-2">
              <span className="text-muted fw-bold" style={{ fontSize: '0.78rem', textTransform: 'uppercase' }}>Scope:</span>
              <select 
                className="form-select form-select-sm"
                value={selectedDocId}
                onChange={(e) => setSelectedDocId(e.target.value)}
              >
                <option value="">Query Entire Repository (All Documents)</option>
                {documents.map(d => (
                  <option key={d.id} value={d.id}>{d.title} (Active: v{d.active_version})</option>
                ))}
              </select>
            </div>
          </div>

          <div className="col-12 col-md-6">
            <div className="d-flex align-items-center gap-2">
              <span className="text-muted fw-bold" style={{ fontSize: '0.78rem', textTransform: 'uppercase' }}>Status Rule:</span>
              <select 
                className="form-select form-select-sm"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <option value="">Automatic (Respect Version Lineage & Intent)</option>
                <option value="Active">Strictly Active Versions Only</option>
                <option value="Superseded">Include Superseded (Historical)</option>
              </select>
            </div>
          </div>

        </div>
      </div>

      {/* Preset Inquiries Bar */}
      <div className="mb-4">
        <span className="text-muted d-block mb-2" style={{ fontSize: '0.74rem', textTransform: 'uppercase', fontWeight: 'bold' }}>
          Hackathon Demo Test Cases:
        </span>
        <div className="d-flex flex-wrap gap-2">
          <button 
            className="query-chip"
            onClick={() => runPreset("What is the current annual leave allowance?")}
          >
            🎯 "What is the current annual leave allowance?" (Current v3.0 = 20d)
          </button>

          <button 
            className="query-chip"
            onClick={() => runPreset("What was the allowance in version 2?")}
          >
            📜 "What was the allowance in version 2?" (Historical v2.0 = 18d)
          </button>

          <button 
            className="query-chip"
            onClick={() => runPreset("Where does the document describe maternity leave?")}
          >
            🔍 "Where does the document describe maternity leave?" (Missing Evidence)
          </button>

          <button 
            className="query-chip"
            onClick={() => runPreset("What changed between version 2 and version 3?")}
          >
            ⚖️ "What changed between version 2 and version 3?" (Comparison)
          </button>
        </div>
      </div>

      {/* Messages Stream Container */}
      <div className="card-ragnext p-4 mb-4" style={{ minHeight: '380px' }}>
        
        {messages.length === 0 ? (
          <div className="text-center py-5 text-muted">
            <Sparkles size={36} className="text-success mb-2" />
            <h5 className="fw-bold text-dark">Ask a Question About Your Documents</h5>
            <p className="mb-0" style={{ maxWidth: '500px', margin: '0 auto', fontSize: '0.88rem' }}>
              The RAGNext engine evaluates document timestamps, resolves superseding chains, eliminates outdated clauses, and provides traceable source citations.
            </p>
          </div>
        ) : (
          <div className="d-flex flex-column gap-4">
            {messages.map((msg) => (
              <div key={msg.id} className={`d-flex flex-column ${msg.role === 'user' ? 'align-items-end' : 'align-items-start'}`}>
                
                {/* User Question Bubble */}
                {msg.role === 'user' ? (
                  <div className="p-3 rounded-3 text-white" style={{ background: '#059669', maxWidth: '80%' }}>
                    <div className="fw-semibold">{msg.content}</div>
                    <div className="text-end text-white-50 mt-1" style={{ fontSize: '0.7rem' }}>{msg.timestamp}</div>
                  </div>
                ) : (
                  /* Assistant Grounded Answer Card */
                  <div className="w-100 p-3 rounded-3 bg-white border" style={{ boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
                    
                    {/* Header Row with Evidence Status & Engine Pill */}
                    <div className="d-flex flex-wrap align-items-center justify-content-between pb-2 mb-2 border-bottom gap-2">
                      <div className="d-flex align-items-center gap-2">
                        <span className={`badge ${
                          msg.evidenceStatus === 'Supported by retrieved evidence' ? 'bg-success' :
                          msg.evidenceStatus === 'Conflicting evidence' ? 'bg-warning text-dark' :
                          msg.evidenceStatus === 'Insufficient evidence' ? 'bg-secondary' : 'bg-info'
                        }`}>
                          {msg.evidenceStatus}
                        </span>
                        <span className="text-muted font-monospace" style={{ fontSize: '0.72rem' }}>
                          Intent: {msg.intent} · {msg.latencyMs}ms
                        </span>
                      </div>
                      <span className="badge bg-light text-muted border font-monospace" style={{ fontSize: '0.68rem' }}>
                        {msg.engine}
                      </span>
                    </div>

                    {/* Conflict Warning Banner if present */}
                    {msg.conflictWarning && (
                      <div className="alert alert-warning py-2 px-3 d-flex align-items-start gap-2 mb-3" style={{ fontSize: '0.84rem' }}>
                        <AlertTriangle size={16} className="text-warning flex-shrink-0 mt-1" />
                        <div>{msg.conflictWarning}</div>
                      </div>
                    )}

                    {/* Main Synthesized Answer Text */}
                    <div className="fw-normal mb-3" style={{ fontSize: '0.94rem', lineHeight: '1.6', color: '#0F172A' }}>
                      {msg.content}
                    </div>

                    {/* Grounded Source Citations & Evidence Excerpts */}
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="mt-3 pt-2 border-top">
                        <div className="d-flex align-items-center gap-1 text-muted mb-2 fw-bold" style={{ fontSize: '0.76rem', textTransform: 'uppercase' }}>
                          <CheckCircle2 size={13} className="text-success" />
                          <span>Verifiable Source Citations ({msg.sources.length}):</span>
                        </div>

                        <div className="d-flex flex-column gap-2">
                          {msg.sources.map((src, sIdx) => (
                            <div key={sIdx} className="evidence-card-box">
                              <div className="evidence-meta-row">
                                <div>
                                  <strong className="text-dark me-2">{src.documentTitle}</strong>
                                  <span className="badge bg-light text-primary border font-monospace me-2">v{src.versionNumber}</span>
                                  <span className="badge bg-white text-muted border font-monospace">Page {src.pageNumber}</span>
                                </div>
                                <StatusBadge status={src.status} />
                              </div>

                              <div className="evidence-text-quote">
                                "{src.evidenceSnippet}"
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                  </div>
                )}

              </div>
            ))}

            {loading && (
              <div className="d-flex align-items-center gap-2 text-muted py-2">
                <span className="spinner-border spinner-border-sm text-success" role="status"></span>
                <span style={{ fontSize: '0.88rem' }}>Analyzing document versions and retrieving verified evidence...</span>
              </div>
            )}
          </div>
        )}

      </div>

      {/* Input Form */}
      <form 
        onSubmit={(e) => { e.preventDefault(); handleSend(); }} 
        className="d-flex gap-2"
      >
        <input 
          type="text" 
          className="form-control form-control-lg"
          placeholder="Ask a question about uploaded policies, manuals, or SOPs..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={loading}
          autoFocus
        />
        <button 
          type="submit" 
          className="btn-green px-4"
          disabled={loading || !question.trim()}
        >
          <Send size={18} />
          <span>Ask</span>
        </button>
      </form>

    </div>
  );
}
