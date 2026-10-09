import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  FileText, 
  Upload, 
  MessageSquare, 
  Settings, 
  Layers, 
  CheckCircle,
  Database,
  Cpu
} from 'lucide-react';
import { api } from '../services/api';

export function Navbar() {
  const location = useLocation();
  const [servicesStatus, setServicesStatus] = useState({ ollama: false, db: true });

  useEffect(() => {
    api.getSettingsStatus()
      .then(res => {
        if (res && res.services) {
          setServicesStatus({
            ollama: res.services.ollama.connected,
            db: res.services.metadataDatabase.connected
          });
        }
      })
      .catch(() => {});
  }, [location.pathname]);

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="navbar-custom">
      <div className="container d-flex align-items-center justify-content-between">
        
        {/* Brand */}
        <div className="d-flex align-items-center gap-3">
          <Link to="/" className="brand-title">
            <Layers className="text-success" size={24} />
            <span>RAG<span className="brand-green">Next</span></span>
          </Link>
          <span className="hackathon-badge">TEAM CYBER KNIGHTS · SH-SVA-04</span>
        </div>

        {/* Nav Links */}
        <div className="d-flex align-items-center gap-1">
          <Link to="/" className={`nav-link-custom ${isActive('/') ? 'active' : ''}`}>
            <Layers size={16} />
            <span>Dashboard</span>
          </Link>

          <Link to="/documents" className={`nav-link-custom ${isActive('/documents') ? 'active' : ''}`}>
            <FileText size={16} />
            <span>Document Library</span>
          </Link>

          <Link to="/upload" className={`nav-link-custom ${isActive('/upload') ? 'active' : ''}`}>
            <Upload size={16} />
            <span>Upload Document</span>
          </Link>

          <Link to="/chat" className={`nav-link-custom ${isActive('/chat') ? 'active' : ''}`}>
            <MessageSquare size={16} />
            <span>AI Document Chat</span>
          </Link>

          <Link to="/settings" className={`nav-link-custom ${isActive('/settings') ? 'active' : ''}`}>
            <Settings size={16} />
            <span>Settings</span>
          </Link>
        </div>

        {/* Local Status Indicator */}
        <div className="d-flex align-items-center gap-2">
          <div className="d-flex align-items-center gap-1 bg-light border px-2 py-1 rounded" style={{ fontSize: '0.75rem', fontFamily: 'monospace' }}>
            <Cpu size={14} className={servicesStatus.ollama ? "text-success" : "text-muted"} />
            <span>{servicesStatus.ollama ? "Ollama Active" : "Deterministic Engine"}</span>
          </div>
        </div>

      </div>
    </nav>
  );
}
