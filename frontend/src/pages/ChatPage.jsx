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
  ChevronUp,
  Trash2,
  Bot,
  User,
  ExternalLink
} from 'lucide-react';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';

/**
 * Lightweight ChatGPT-style Markdown formatter for crisp, structured reading
 */
function FormattedMarkdown({ content }) {
  if (!content) return null;

  const renderInline = (text) => {
    // Splits by **bold**, *italic*, `code`
    const regex = /(\*\*.*?\*\*|\*.*?\*|`.*?`)/g;
    const parts = text.split(regex);

    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} className="text-dark fw-bold">{part.slice(2, -2)}</strong>;
      }
      if (part.startsWith('*') && part.endsWith('*')) {
        return <em key={i} className="text-secondary">{part.slice(1, -1)}</em>;
      }
      if (part.startsWith('`') && part.endsWith('`')) {
        return (
          <code key={i} className="bg-light px-2 py-0.5 rounded text-success font-monospace" style={{ fontSize: '0.86em' }}>
            {part.slice(1, -1)}
          </code>
        );
      }
      return part;
    });
  };

  const lines = content.split('\n');
  const elements = [];
  let currentList = [];

  const flushList = () => {
    if (currentList.length > 0) {
      elements.push(
        <ul key={`ul-${elements.length}`} className="my-2 ps-3" style={{ listStyleType: 'disc' }}>
          {currentList.map((item, idx) => (
            <li key={idx} className="mb-2" style={{ lineHeight: '1.6', color: '#1E293B' }}>
              {renderInline(item)}
            </li>
          ))}
        </ul>
      );
      currentList = [];
    }
  };

  for (let i = 0; i < lines.length; i++) {
    const rawLine = lines[i];
    const line = rawLine.trim();

    if (!line) {
      flushList();
      continue;
    }

    if (line.startsWith('### ')) {
      flushList();
      elements.push(
        <h6 key={`h3-${i}`} className="fw-bold mt-3 mb-2 text-dark d-flex align-items-center gap-2" style={{ fontSize: '1.05rem', letterSpacing: '-0.2px' }}>
          {renderInline(line.replace('### ', ''))}
        </h6>
      );
    } else if (line.startsWith('## ')) {
      flushList();
      elements.push(
        <h5 key={`h2-${i}`} className="fw-bold mt-3 mb-2 text-dark" style={{ fontSize: '1.15rem' }}>
          {renderInline(line.replace('## ', ''))}
        </h5>
      );
    } else if (line.startsWith('- ') || line.startsWith('* ')) {
      currentList.push(line.substring(2));
    } else if (line.startsWith('> ')) {
      flushList();
      elements.push(
        <div key={`quote-${i}`} className="border-start border-3 border-success ps-3 py-2 my-2 bg-light rounded-end" style={{ fontSize: '0.92rem', color: '#334155' }}>
          {renderInline(line.substring(2))}
        </div>
      );
    } else {
      flushList();
      elements.push(
        <p key={`p-${i}`} className="mb-2" style={{ lineHeight: '1.65', color: '#1E293B', fontSize: '0.96rem' }}>
          {renderInline(line)}
        </p>
      );
    }
  }
  flushList();

  return <div className="chatgpt-formatted-body">{elements}</div>;
}

/**
 * Assistant response bubble with ChatGPT aesthetics and collapsible evidence drawer
 */
function AssistantMessageCard({ msg }) {
  const [showSources, setShowSources] = useState(false);

  const isSupported = msg.evidenceStatus === 'Supported by retrieved evidence';
  const isConflicting = msg.evidenceStatus === 'Conflicting evidence';
  const isInsufficient = msg.evidenceStatus === 'Insufficient evidence';

  return (
    <div className="w-100 p-4 rounded-4 bg-white border" style={{ boxShadow: '0 2px 10px rgba(0,0,0,0.03)', maxWidth: '920px' }}>
      
      {/* Bot Identity Header */}
      <div className="d-flex flex-wrap align-items-center justify-content-between pb-3 mb-3 border-bottom gap-2">
        <div className="d-flex align-items-center gap-2">
          <div className="d-flex align-items-center justify-content-center rounded-circle text-white bg-success" style={{ width: '32px', height: '32px' }}>
            <Sparkles size={16} />
          </div>
          <div>
            <div className="fw-bold text-dark" style={{ fontSize: '0.92rem', lineHeight: '1.2' }}>
              RAGNext Assistant
            </div>
            <div className="text-muted" style={{ fontSize: '0.74rem' }}>
              Version-Aware Document Intelligence
            </div>
          </div>
        </div>

        <div className="d-flex align-items-center gap-2">
          <span className={`badge ${
            isSupported ? 'bg-success-subtle text-success border border-success-subtle' :
            isConflicting ? 'bg-warning-subtle text-warning border border-warning-subtle' :
            isInsufficient ? 'bg-secondary-subtle text-secondary border border-secondary-subtle' :
            'bg-info-subtle text-info border border-info-subtle'
          } rounded-pill px-2.5 py-1`} style={{ fontSize: '0.72rem', fontWeight: 600 }}>
            {msg.evidenceStatus}
          </span>
          <span className="badge bg-light text-muted border font-monospace" style={{ fontSize: '0.7rem' }}>
            {msg.engine}
          </span>
        </div>
      </div>

      {/* Conflict Alert (if any) */}
      {msg.conflictWarning && (
        <div className="alert alert-warning py-2.5 px-3 d-flex align-items-start gap-2 mb-3 rounded-3" style={{ fontSize: '0.86rem' }}>
          <AlertTriangle size={17} className="text-warning flex-shrink-0 mt-0.5" />
          <div>{msg.conflictWarning}</div>
        </div>
      )}

      {/* Structured ChatGPT Answer */}
      <div className="mb-3">
        <FormattedMarkdown content={msg.content} />
      </div>

      {/* Collapsible Verifiable Source Citations */}
      {msg.sources && msg.sources.length > 0 && (
        <div className="mt-3 pt-3 border-top">
          <button 
            type="button"
            className="btn btn-sm btn-light border d-flex align-items-center justify-content-between w-100 py-2 px-3 rounded-3"
            onClick={() => setShowSources(prev => !prev)}
            style={{ fontSize: '0.82rem', fontWeight: 600, color: '#475569' }}
          >
            <div className="d-flex align-items-center gap-2">
              <CheckCircle2 size={15} className="text-success" />
              <span>Verified Source Citations ({msg.sources.length} excerpt{msg.sources.length > 1 ? 's' : ''})</span>
            </div>
            <div className="d-flex align-items-center gap-1 text-muted" style={{ fontSize: '0.76rem' }}>
              <span>{showSources ? 'Hide Sources' : 'Show Sources'}</span>
              {showSources ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </div>
          </button>

          {showSources && (
            <div className="d-flex flex-column gap-2 mt-3 animate-fade-in">
              {msg.sources.map((src, sIdx) => (
                <div key={sIdx} className="evidence-card-box p-3 bg-light rounded-3 border-start border-3 border-success">
                  <div className="d-flex align-items-center justify-content-between mb-2">
                    <div className="d-flex align-items-center gap-2">
                      <strong className="text-dark" style={{ fontSize: '0.86rem' }}>{src.documentTitle}</strong>
                      <span className="badge bg-white text-primary border font-monospace">v{src.versionNumber}</span>
                      <span className="badge bg-white text-muted border font-monospace">Page {src.pageNumber}</span>
                    </div>
                    <StatusBadge status={src.status} />
                  </div>
                  <div className="evidence-text-quote text-secondary font-monospace" style={{ fontSize: '0.82rem', lineHeight: '1.5' }}>
                    "{src.evidenceSnippet}"
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

    </div>
  );
}

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
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
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
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => [...prev, botMsg]);
      } else {
        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          role: 'assistant',
          content: `### ⚠️ Error\n\n${res.error || 'Failed to generate answer from documents.'}`,
          evidenceStatus: 'Error',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }]);
      }
    } catch (e) {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        content: `### ⚠️ Network Disconnection\n\nCould not reach the local RAGNext backend engine. Please check if the backend server is running.`,
        evidenceStatus: 'Error',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
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
            Version-aware natural conversation grounded with verifiable document citations.
          </p>
        </div>
        <div className="d-flex align-items-center gap-2">
          {messages.length > 0 && (
            <button className="btn btn-outline-secondary btn-sm d-flex align-items-center gap-1 rounded-pill px-3" onClick={clearChat}>
              <Trash2 size={14} />
              <span>Clear Chat</span>
            </button>
          )}
        </div>
      </div>

      {/* Scope and Retrieval Filters Bar */}
      <div className="card-ragnext p-3 mb-4 bg-light rounded-4">
        <div className="row g-2 align-items-center">
          
          <div className="col-12 col-md-6">
            <div className="d-flex align-items-center gap-2">
              <span className="text-muted fw-bold" style={{ fontSize: '0.78rem', textTransform: 'uppercase' }}>Scope:</span>
              <select 
                className="form-select form-select-sm rounded-pill"
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
              <span className="text-muted fw-bold" style={{ fontSize: '0.78rem', textTransform: 'uppercase' }}>Version Rule:</span>
              <select 
                className="form-select form-select-sm rounded-pill"
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
          Quick Demo Questions:
        </span>
        <div className="d-flex flex-wrap gap-2">
          <button 
            className="query-chip"
            onClick={() => runPreset("Can I use my personal laptop for remote work?")}
          >
            💻 "Can I use my personal laptop for remote work?"
          </button>

          <button 
            className="query-chip"
            onClick={() => runPreset("What are the password requirements and is 2FA mandatory?")}
          >
            🔑 "What are the password requirements and is 2FA mandatory?"
          </button>

          <button 
            className="query-chip"
            onClick={() => runPreset("What is the current annual leave allowance?")}
          >
            🎯 "What is the current annual leave allowance?" (v3.0 = 20d)
          </button>

          <button 
            className="query-chip"
            onClick={() => runPreset("What was the allowance in version 2?")}
          >
            📜 "What was the allowance in version 2?" (Historical v2.0 = 18d)
          </button>
        </div>
      </div>

      {/* Messages Stream Container */}
      <div className="card-ragnext p-4 mb-4 rounded-4" style={{ minHeight: '380px', background: '#F8FAFC' }}>
        
        {messages.length === 0 ? (
          <div className="text-center py-5 text-muted">
            <Sparkles size={40} className="text-success mb-2" />
            <h5 className="fw-bold text-dark">How can I help you today?</h5>
            <p className="mb-0" style={{ maxWidth: '540px', margin: '0 auto', fontSize: '0.9rem', color: '#64748B' }}>
              Ask anything about your policies, manuals, or compliance guidelines. Answers are structured, friendly, and cited to exact verified document versions.
            </p>
          </div>
        ) : (
          <div className="d-flex flex-column gap-4">
            {messages.map((msg) => (
              <div key={msg.id} className={`d-flex flex-column ${msg.role === 'user' ? 'align-items-end' : 'align-items-start'}`}>
                
                {/* User Message Bubble */}
                {msg.role === 'user' ? (
                  <div className="d-flex align-items-start gap-2" style={{ maxWidth: '82%' }}>
                    <div className="p-3 px-4 rounded-4 text-white" style={{ background: '#059669', boxShadow: '0 2px 6px rgba(5,150,105,0.2)' }}>
                      <div className="fw-medium" style={{ fontSize: '0.96rem' }}>{msg.content}</div>
                      <div className="text-end text-white-50 mt-1" style={{ fontSize: '0.68rem' }}>{msg.timestamp}</div>
                    </div>
                    <div className="d-flex align-items-center justify-content-center rounded-circle bg-light border text-success flex-shrink-0 mt-1" style={{ width: '32px', height: '32px' }}>
                      <User size={16} />
                    </div>
                  </div>
                ) : (
                  /* Assistant Grounded ChatGPT Card */
                  <AssistantMessageCard msg={msg} />
                )}

              </div>
            ))}

            {loading && (
              <div className="d-flex align-items-center gap-3 p-3 bg-white border rounded-4 shadow-sm" style={{ maxWidth: '420px' }}>
                <div className="spinner-border spinner-border-sm text-success" role="status"></div>
                <div style={{ fontSize: '0.88rem', color: '#334155' }}>
                  Consulting version lineage and drafting answer...
                </div>
              </div>
            )}
          </div>
        )}

      </div>

      {/* Input Form (ChatGPT pill-style input) */}
      <form 
        onSubmit={(e) => { e.preventDefault(); handleSend(); }} 
        className="d-flex gap-2 p-2 bg-white border rounded-pill shadow-sm"
      >
        <input 
          type="text" 
          className="form-control border-0 bg-transparent px-4 shadow-none"
          placeholder="Ask anything about your documents..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={loading}
          autoFocus
          style={{ fontSize: '0.96rem' }}
        />
        <button 
          type="submit" 
          className="btn-green rounded-circle d-flex align-items-center justify-content-center flex-shrink-0"
          style={{ width: '42px', height: '42px', padding: 0 }}
          disabled={loading || !question.trim()}
        >
          <Send size={16} />
        </button>
      </form>

    </div>
  );
}
