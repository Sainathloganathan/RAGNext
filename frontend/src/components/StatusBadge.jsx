import React from 'react';

export function StatusBadge({ status }) {
  const norm = (status || 'Draft').toLowerCase();

  if (norm === 'active') {
    return <span className="status-pill active-status">● Active</span>;
  }
  if (norm === 'superseded') {
    return <span className="status-pill superseded-status">✖ Superseded</span>;
  }
  if (norm === 'draft') {
    return <span className="status-pill draft-status">✎ Draft</span>;
  }
  if (norm === 'archived' || norm === 'expired') {
    return <span className="status-pill archived-status">⧗ {status}</span>;
  }

  return <span className="status-pill draft-status">{status}</span>;
}

export function FormatBadge({ format }) {
  const ext = (format || 'pdf').toLowerCase().replace('.', '');
  return <span className={`fmt-badge ${ext}`}>{ext.toUpperCase()}</span>;
}
