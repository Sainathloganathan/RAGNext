import express from 'express';
import cors from 'cors';
import { config } from './config/env.js';
import healthRoutes from './routes/healthRoutes.js';
import dashboardRoutes from './routes/dashboardRoutes.js';
import documentRoutes from './routes/documentRoutes.js';
import versionRoutes from './routes/versionRoutes.js';
import processingRoutes from './routes/processingRoutes.js';
import chatRoutes from './routes/chatRoutes.js';
import settingsRoutes from './routes/settingsRoutes.js';
import demoRoutes from './routes/demoRoutes.js';
import { errorHandler } from './middleware/errorHandler.js';

const app = express();

// Security & Parsing Middleware
app.use(cors({
  origin: '*', // Allow frontend Vite client
  methods: ['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Static uploads serving for document preview
app.use('/uploads', express.static(config.storageDir));

// API Routes
app.use('/api/health', healthRoutes);
app.use('/api/dashboard', dashboardRoutes);
app.use('/api/documents', documentRoutes);
app.use('/api', versionRoutes);
app.use('/api/processing', processingRoutes);
app.use('/api/chat', chatRoutes);
app.use('/api/settings', settingsRoutes);
app.use('/api/demo', demoRoutes);

// Root Welcome endpoint
app.get('/', (req, res) => {
  res.json({
    name: 'RAGNext Backend API',
    team: 'Cyber Knights',
    problemStatement: 'SH-SVA-04',
    version: '1.0.0',
    docs: '/api/health'
  });
});

// Centralized Error Handler
app.use(errorHandler);

export default app;
