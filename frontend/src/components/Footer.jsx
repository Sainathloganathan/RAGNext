import React from 'react';
import { Shield, HardDrive, CheckCircle } from 'lucide-react';

export function Footer() {
  return (
    <footer className="footer-custom">
      <div className="container d-flex flex-wrap align-items-center justify-content-between gap-3">
        <div className="d-flex align-items-center gap-2">
          <strong>RAGNext</strong> — <span>Advanced Version-Aware RAG Solution for Domain-Specific Intelligence</span>
        </div>
        <div className="d-flex align-items-center gap-3">
          <span className="d-flex align-items-center gap-1 text-success">
            <CheckCircle size={14} /> Offline-First Architecture
          </span>
          <span className="d-flex align-items-center gap-1">
            <Shield size={14} /> Zero Hallucination Guardrails
          </span>
          <span className="text-muted">Cyber Knights (SH-SVA-04)</span>
        </div>
      </div>
    </footer>
  );
}
