import app from './app.js';
import { config } from './config/env.js';
import { initDatabase } from './database/db.js';
import { runMigrations } from './database/migrations.js';

async function startServer() {
  try {
    console.log('🚀 Initializing RAGNext Backend Engine (Cyber Knights — SH-SVA-04)...');
    
    // 1. Initialize Database Adapter
    await initDatabase();

    // 2. Run Schema Migrations
    await runMigrations();

    // 3. Start Express HTTP Server
    const server = app.listen(config.port, () => {
      console.log(`=======================================================`);
      console.log(`✅ RAGNext Backend Server is listening on port ${config.port}`);
      console.log(`🔗 Health Check: http://localhost:${config.port}/api/health`);
      console.log(`⚙️  Environment: ${config.nodeEnv}`);
      console.log(`📁 Upload Storage: ${config.storageDir}`);
      console.log(`=======================================================`);
    });

    return server;
  } catch (err) {
    console.error('❌ Failed to start RAGNext backend server:', err);
    process.exit(1);
  }
}

startServer();
