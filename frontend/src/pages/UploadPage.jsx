import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  UploadCloud, 
  FileCheck, 
  AlertCircle, 
  CheckCircle2, 
  Loader2,
  Calendar,
  Layers,
  ArrowRight
} from 'lucide-react';
import { api } from '../services/api';

export function UploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('Human Resources');
  const [versionNumber, setVersionNumber] = useState('1.0');
  const [status, setStatus] = useState('Active');
  const [effectiveDate, setEffectiveDate] = useState(new Date().toISOString().split('T')[0]);
  const [expirationDate, setExpirationDate] = useState('');
  const [description, setDescription] = useState('');
  const [existingDocs, setExistingDocs] = useState([]);
  const [selectedDocId, setSelectedDocId] = useState('');

  const [uploading, setUploading] = useState(false);
  const [jobInfo, setJobInfo] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  useEffect(() => {
    api.getDocuments()
      .then(res => {
        if (res.success) setExistingDocs(res.documents || []);
      })
      .catch(() => {});
  }, []);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      if (!title) {
        setTitle(selected.name.replace(/\.[^/.]+$/, ''));
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setErrorMsg('Please select a file to upload.');
      return;
    }

    setUploading(true);
    setErrorMsg(null);
    setJobInfo({ progress: 10, step: 'Uploading file to storage gateway...' });

    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    formData.append('category', category);
    formData.append('versionNumber', versionNumber);
    formData.append('status', status);
    formData.append('effectiveDate', effectiveDate);
    formData.append('expirationDate', expirationDate);
    formData.append('description', description);

    if (selectedDocId) {
      const parentDoc = existingDocs.find(d => d.id === selectedDocId);
      if (parentDoc) {
        formData.append('documentId', parentDoc.id);
        formData.append('groupId', parentDoc.group_id);
      }
    }

    try {
      const res = await api.uploadDocument(formData);
      if (res.success && res.jobId) {
        // Poll job progress
        pollProcessingJob(res.jobId, res.documentId);
      } else {
        setErrorMsg(res.error || 'Failed to upload document.');
        setUploading(false);
      }
    } catch (err) {
      setErrorMsg(err.message || 'Upload request failed.');
      setUploading(false);
    }
  };

  const pollProcessingJob = (jobId, documentId) => {
    const interval = setInterval(async () => {
      try {
        const res = await api.getProcessingJob(jobId);
        if (res.success && res.job) {
          setJobInfo(res.job);
          if (res.job.status === 'Completed') {
            clearInterval(interval);
            setTimeout(() => {
              navigate(`/documents/${documentId}/versions`);
            }, 1200);
          } else if (res.job.status === 'Failed') {
            clearInterval(interval);
            setErrorMsg(`Processing failed: ${res.job.error_message}`);
            setUploading(false);
          }
        }
      } catch (e) {
        clearInterval(interval);
        setUploading(false);
      }
    }, 800);
  };

  return (
    <div className="container" style={{ maxWidth: '840px' }}>
      
      <div className="mb-4 pb-3 border-bottom">
        <h2 className="fw-bold mb-1">Upload & Ingest Document</h2>
        <p className="text-muted mb-0" style={{ fontSize: '0.9rem' }}>
          Extract text, generate semantic chunks, create local embeddings, and track document version lineage.
        </p>
      </div>

      {errorMsg && (
        <div className="alert alert-danger d-flex align-items-center gap-2 mb-4" role="alert">
          <AlertCircle size={18} />
          <span>{errorMsg}</span>
        </div>
      )}

      {uploading ? (
        <div className="card-ragnext p-5 text-center">
          <Loader2 size={40} className="text-success spinner-border mb-3" style={{ animation: 'spin 1s linear infinite' }} />
          <h4 className="fw-bold mb-2">Processing Document Pipeline</h4>
          <p className="text-muted mb-4">{jobInfo?.step || 'Extracting and indexing...'}</p>

          <div className="progress mb-3" style={{ height: '12px' }}>
            <div 
              className="progress-bar bg-success progress-bar-striped progress-bar-animated" 
              role="progressbar" 
              style={{ width: `${jobInfo?.progress || 20}%` }}
            ></div>
          </div>

          <div className="font-monospace text-muted" style={{ fontSize: '0.8rem' }}>
            Stage: {jobInfo?.step} ({jobInfo?.progress || 20}%)
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="card-ragnext p-4">
          
          {/* Dropzone */}
          <div className="mb-4">
            <label className="form-label fw-bold">Select Document File</label>
            <div 
              className="border border-2 border-dashed rounded-3 p-4 text-center bg-light"
              style={{ borderColor: file ? '#10B981' : '#CBD5E1', cursor: 'pointer' }}
              onClick={() => document.getElementById('fileInput').click()}
            >
              <UploadCloud size={36} className={file ? "text-success mb-2" : "text-muted mb-2"} />
              {file ? (
                <div>
                  <div className="fw-bold text-success">{file.name}</div>
                  <small className="text-muted">{(file.size / 1024).toFixed(1)} KB — Ready for extraction</small>
                </div>
              ) : (
                <div>
                  <div className="fw-bold text-dark">Click or drag document to this area</div>
                  <small className="text-muted">Supported formats: PDF, DOCX, PPTX, TXT (Max: 25MB)</small>
                </div>
              )}
              <input 
                type="file" 
                id="fileInput" 
                className="d-none" 
                accept=".pdf,.docx,.doc,.pptx,.ppt,.txt,.md"
                onChange={handleFileChange}
              />
            </div>
          </div>

          {/* Document Grouping / Link to Existing */}
          <div className="mb-3">
            <label className="form-label fw-bold">Document Family / Group</label>
            <select 
              className="form-select"
              value={selectedDocId}
              onChange={(e) => setSelectedDocId(e.target.value)}
            >
              <option value="">Create as a New Document</option>
              {existingDocs.map(d => (
                <option key={d.id} value={d.id}>Add as a new revision to: {d.title} (Current: v{d.active_version})</option>
              ))}
            </select>
            <small className="text-muted">Select an existing document if uploading a newer revision of the same policy or manual.</small>
          </div>

          {/* Form Fields */}
          <div className="row g-3 mb-3">
            
            <div className="col-12 col-md-8">
              <label className="form-label fw-bold">Document Title</label>
              <input 
                type="text" 
                className="form-control" 
                placeholder="e.g. Travel and Expense Reimbursement Policy"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>

            <div className="col-12 col-md-4">
              <label className="form-label fw-bold">Category</label>
              <select 
                className="form-select"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              >
                <option value="Human Resources">Human Resources</option>
                <option value="Engineering & Safety">Engineering & Safety</option>
                <option value="Finance & Compliance">Finance & Compliance</option>
                <option value="Healthcare & Clinical">Healthcare & Clinical</option>
                <option value="Legal & Regulatory">Legal & Regulatory</option>
                <option value="General">General</option>
              </select>
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label fw-bold">Version Number</label>
              <input 
                type="text" 
                className="form-control font-monospace" 
                placeholder="e.g. 1.0, 2.4, 3.0"
                value={versionNumber}
                onChange={(e) => setVersionNumber(e.target.value)}
                required
              />
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label fw-bold">Initial Version Status</label>
              <select 
                className="form-select"
                value={status}
                onChange={(e) => setStatus(e.target.value)}
              >
                <option value="Active">Active (Eligible for current queries)</option>
                <option value="Draft">Draft (Under review)</option>
                <option value="Superseded">Superseded (Historical only)</option>
                <option value="Archived">Archived</option>
              </select>
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label fw-bold">Effective Date</label>
              <input 
                type="date" 
                className="form-control" 
                value={effectiveDate}
                onChange={(e) => setEffectiveDate(e.target.value)}
              />
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label fw-bold">Expiration Date (Optional)</label>
              <input 
                type="date" 
                className="form-control" 
                value={expirationDate}
                onChange={(e) => setExpirationDate(e.target.value)}
              />
            </div>

            <div className="col-12">
              <label className="form-label fw-bold">Version Notes / Description</label>
              <textarea 
                className="form-control" 
                rows="2" 
                placeholder="Describe key changes introduced in this revision..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              ></textarea>
            </div>

          </div>

          <button type="submit" className="btn-green w-100 justify-content-center py-2">
            <CheckCircle2 size={18} />
            <span>Upload & Process Document Pipeline</span>
          </button>

        </form>
      )}

    </div>
  );
}
