import multer from 'multer';
import path from 'path';
import fs from 'fs';
import crypto from 'crypto';
import { config } from '../config/env.js';

// Ensure storage directory exists
if (!fs.existsSync(config.storageDir)) {
  fs.mkdirSync(config.storageDir, { recursive: true });
}

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, config.storageDir);
  },
  filename: function (req, file, cb) {
    const ext = path.extname(file.originalname).toLowerCase();
    const safeHash = crypto.randomBytes(8).toString('hex');
    const safeName = `doc_${Date.now()}_${safeHash}${ext}`;
    cb(null, safeName);
  }
});

const fileFilter = (req, file, cb) => {
  const allowedExts = ['.pdf', '.docx', '.doc', '.pptx', '.ppt', '.txt', '.md'];
  const ext = path.extname(file.originalname).toLowerCase();

  if (allowedExts.includes(ext)) {
    cb(null, true);
  } else {
    cb(new Error(`UNSUPPORTED_FILE_TYPE: Only PDF, DOCX, PPTX, and TXT files are supported. Provided: ${ext}`), false);
  }
};

export const upload = multer({
  storage,
  limits: {
    fileSize: config.maxUploadSizeMb * 1024 * 1024 // e.g. 25MB
  },
  fileFilter
});
