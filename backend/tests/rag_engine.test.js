import assert from 'assert';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import { initDatabase, db } from '../src/database/db.js';
import { runMigrations } from '../src/database/migrations.js';
import { documentRepository } from '../src/repositories/documentRepository.js';
import { extractDocumentText } from '../src/document-processing/extractors.js';
import { chunkDocumentPages } from '../src/document-processing/chunker.js';
import { vectorStore } from '../src/retrieval/vector_store.js';
import { versionRules } from '../src/rag/version_rules.js';
import { generateGroundedAnswer } from '../src/rag/answer_generator.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function runRAGTestSuite() {
  console.log('\n======================================================');
  console.log('🧪 RUNNING CYBER KNIGHTS RAGNEXT AUTOMATED TEST SUITE');
  console.log('======================================================\n');

  let passedTests = 0;
  let totalTests = 0;

  function test(name, fn) {
    totalTests++;
    return (async () => {
      try {
        await fn();
        console.log(`  ✅ PASS: ${name}`);
        passedTests++;
      } catch (err) {
        console.error(`  ❌ FAIL: ${name}`);
        console.error(`     Error: ${err.message}\n`);
      }
    })();
  }

  // 1. Initialize Test DB
  await initDatabase();
  await runMigrations();
  await vectorStore.resetAll();

  // Test 1: Document & Group Creation
  await test('Document metadata validation and repository storage', async () => {
    const groupId = 'test_grp_hr';
    const docId = 'test_doc_leave';

    await documentRepository.createGroup({
      id: groupId,
      name: 'HR Policies Group',
      description: 'Corporate HR manuals',
      category: 'Human Resources',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    });

    await documentRepository.createDocument({
      id: docId,
      group_id: groupId,
      title: 'Leave Policy Manual',
      category: 'Human Resources',
      created_at: new Date().toISOString()
    });

    const doc = await documentRepository.getDocumentById(docId);
    assert.ok(doc, 'Document should exist');
    assert.strictEqual(doc.title, 'Leave Policy Manual');
  });

  // Test 2: Ingest 3 Versions (v1.0 = 15 days, v2.0 = 18 days, v3.0 = 20 days)
  await test('Ingest 3 document revisions with temporal metadata', async () => {
    const docId = 'test_doc_leave';
    const groupId = 'test_grp_hr';

    // v1: 15 days (Superseded)
    const v1Text = 'Under Leave Policy v1.0, employees are entitled to an annual leave allowance of 15 days.';
    const v1 = {
      id: 'test_ver_1',
      document_id: docId,
      group_id: groupId,
      version_number: '1.0',
      status: 'Superseded',
      file_name: 'leave_v1.txt',
      file_path: '/tmp/leave_v1.txt',
      file_size: 100,
      mime_type: 'text/plain',
      checksum: 'hash1',
      effective_date: '2021-01-01',
      expiration_date: '2022-12-31',
      description: 'v1.0',
      uploaded_at: new Date('2021-01-01').toISOString(),
      processing_status: 'Indexed'
    };
    await documentRepository.createVersion(v1);
    const c1 = chunkDocumentPages([{ pageNumber: 1, text: v1Text }], {
      versionId: v1.id,
      documentId: docId,
      groupId,
      documentTitle: 'Leave Policy Manual',
      versionNumber: '1.0',
      status: 'Superseded'
    });
    await documentRepository.saveChunks(c1);
    await vectorStore.indexChunks(c1);

    // v2: 18 days (Superseded)
    const v2Text = 'Under Leave Policy v2.0, employees are entitled to an annual leave allowance of 18 days.';
    const v2 = {
      id: 'test_ver_2',
      document_id: docId,
      group_id: groupId,
      version_number: '2.0',
      status: 'Superseded',
      file_name: 'leave_v2.txt',
      file_path: '/tmp/leave_v2.txt',
      file_size: 100,
      mime_type: 'text/plain',
      checksum: 'hash2',
      effective_date: '2023-01-01',
      expiration_date: '2024-12-31',
      description: 'v2.0',
      uploaded_at: new Date('2023-01-01').toISOString(),
      processing_status: 'Indexed'
    };
    await documentRepository.createVersion(v2);
    const c2 = chunkDocumentPages([{ pageNumber: 2, text: v2Text }], {
      versionId: v2.id,
      documentId: docId,
      groupId,
      documentTitle: 'Leave Policy Manual',
      versionNumber: '2.0',
      status: 'Superseded'
    });
    await documentRepository.saveChunks(c2);
    await vectorStore.indexChunks(c2);

    // v3: 20 days (Active)
    const v3Text = 'Under Leave Policy v3.0, employees are entitled to an annual leave allowance of 20 days per calendar year.';
    const v3 = {
      id: 'test_ver_3',
      document_id: docId,
      group_id: groupId,
      version_number: '3.0',
      status: 'Active',
      file_name: 'leave_v3.txt',
      file_path: '/tmp/leave_v3.txt',
      file_size: 100,
      mime_type: 'text/plain',
      checksum: 'hash3',
      effective_date: '2025-01-01',
      expiration_date: null,
      description: 'v3.0 Current',
      uploaded_at: new Date('2025-01-01').toISOString(),
      processing_status: 'Indexed'
    };
    await documentRepository.createVersion(v3);
    const c3 = chunkDocumentPages([{ pageNumber: 4, text: v3Text }], {
      versionId: v3.id,
      documentId: docId,
      groupId,
      documentTitle: 'Leave Policy Manual',
      versionNumber: '3.0',
      status: 'Active'
    });
    await documentRepository.saveChunks(c3);
    await vectorStore.indexChunks(c3);

    const versions = await documentRepository.getVersionsByDocumentId(docId);
    assert.strictEqual(versions.length, 3, 'Should have 3 versions');
  });

  // Test 3: Current-Version Query ("What is the current annual leave allowance?")
  await test('Current-version query retrieves strictly active version (v3.0 = 20 days)', async () => {
    const query = 'What is the current annual leave allowance?';
    const allVersions = await documentRepository.getVersionsByDocumentId('test_doc_leave');
    const intentInfo = versionRules.classifyQueryIntent(query);
    assert.strictEqual(intentInfo.intent, 'CURRENT', 'Intent should be CURRENT');

    const { eligibleVersions, conflictWarning } = versionRules.resolveEligibleVersions(allVersions, intentInfo);
    assert.strictEqual(eligibleVersions.length, 1, 'Should have 1 eligible active version');
    assert.strictEqual(eligibleVersions[0].version_number, '3.0', 'Active version must be 3.0');
    assert.strictEqual(conflictWarning, null, 'No conflict should be detected');

    const chunks = await vectorStore.search(query, { versionIds: eligibleVersions.map(v => v.id) });
    assert.ok(chunks.length > 0, 'Should retrieve chunks from v3.0');

    const result = await generateGroundedAnswer(query, chunks, { intentInfo, conflictWarning, eligibleVersions });
    assert.ok(result.answer.includes('20 days'), 'Answer must state 20 days');
    assert.ok(!result.answer.includes('15 days') && !result.answer.includes('18 days'), 'Answer must not cite v1 or v2 as current');
    assert.strictEqual(result.sources[0].versionNumber, '3.0', 'Source citation must reference v3.0');
    assert.strictEqual(result.sources[0].pageNumber, 4, 'Source citation page number must be 4');
  });

  // Test 4: Historical Query ("What was the allowance in version 2?")
  await test('Historical query retrieves requested historical version (v2.0 = 18 days)', async () => {
    const query = 'What was the allowance in version 2?';
    const allVersions = await documentRepository.getVersionsByDocumentId('test_doc_leave');
    const intentInfo = versionRules.classifyQueryIntent(query);
    assert.strictEqual(intentInfo.intent, 'HISTORICAL', 'Intent should be HISTORICAL');

    const { eligibleVersions } = versionRules.resolveEligibleVersions(allVersions, intentInfo);
    assert.ok(eligibleVersions.some(v => v.version_number === '2.0'), 'Should include v2.0');

    const chunks = await vectorStore.search(query, { versionIds: eligibleVersions.map(v => v.id) });
    const result = await generateGroundedAnswer(query, chunks, { intentInfo, eligibleVersions });
    assert.ok(result.answer.includes('18 days'), 'Answer must reflect v2.0 content (18 days)');
    assert.strictEqual(result.sources[0].versionNumber, '2.0');
  });

  // Test 5: Missing Evidence ("Where does the document describe maternity leave?")
  await test('Missing evidence handling returns honest insufficient evidence report', async () => {
    const query = 'Where does the document describe maternity leave?';
    const allVersions = await documentRepository.getVersionsByDocumentId('test_doc_leave');
    const intentInfo = versionRules.classifyQueryIntent(query);
    const { eligibleVersions } = versionRules.resolveEligibleVersions(allVersions, intentInfo);

    const chunks = await vectorStore.search(query, { versionIds: eligibleVersions.map(v => v.id), minScore: 0.6 });
    const result = await generateGroundedAnswer(query, chunks, { intentInfo, eligibleVersions });
    assert.strictEqual(result.evidenceStatus, 'Insufficient evidence', 'Must return Insufficient evidence status');
    assert.ok(result.answer.toLowerCase().includes('insufficient evidence'), 'Must clearly report lack of evidence');
  });

  // Test 6: Conflicting Active Versions Detection
  await test('Conflicting active versions detection flags conflict rather than silently guessing', async () => {
    // Manually mark version 2.0 as Active as well to simulate admin conflict
    await documentRepository.updateVersionStatus('test_ver_2', 'Active');
    
    const query = 'What is our current leave policy?';
    const allVersions = await documentRepository.getVersionsByDocumentId('test_doc_leave');
    const intentInfo = versionRules.classifyQueryIntent(query);
    const { eligibleVersions, conflictWarning } = versionRules.resolveEligibleVersions(allVersions, intentInfo);

    assert.ok(conflictWarning, 'Conflict warning must be generated');
    assert.ok(conflictWarning.includes('CONFLICT DETECTED'), 'Warning text must mention conflict');
    assert.strictEqual(eligibleVersions.length, 2, 'Both conflicting active versions must be surfaced for inspection');

    // Reset v2 back to Superseded
    await documentRepository.updateVersionStatus('test_ver_2', 'Superseded');
  });

  // Test 7: Deletion Cleanup
  await test('Document deletion properly cleans up metadata and vector chunks', async () => {
    await vectorStore.deleteByDocumentId('test_doc_leave');
    await documentRepository.deleteDocument('test_doc_leave');
    
    const doc = await documentRepository.getDocumentById('test_doc_leave');
    assert.strictEqual(doc, null, 'Document should be deleted');
    const chunks = await vectorStore.search('annual leave', { documentId: 'test_doc_leave' });
    assert.strictEqual(chunks.length, 0, 'Vector chunks should be purged');
  });

  console.log('\n------------------------------------------------------');
  console.log(`📊 SUMMARY: ${passedTests} of ${totalTests} tests passed (${Math.round((passedTests / totalTests) * 100)}%)`);
  console.log('------------------------------------------------------\n');
}

runRAGTestSuite().catch(err => {
  console.error('Fatal Test Error:', err);
  process.exit(1);
});
