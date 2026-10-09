import crypto from 'crypto';
import { config } from '../config/env.js';

/**
 * Splits extracted document pages into semantic chunks with metadata
 */
export function chunkDocumentPages(pages, metadata = {}) {
  const chunkSize = config.chunkSize || 500;
  const chunkOverlap = config.chunkOverlap || 100;
  const chunks = [];
  let chunkIndex = 0;

  for (const page of pages) {
    const pageNum = page.pageNumber || 1;
    const pageText = page.text || '';

    // Split page text into sentences / logical units
    const sentences = pageText.split(/(?<=[.?!])\s+|\n\n+/).filter(s => s.trim().length > 0);

    let currentChunkText = '';
    let currentSection = page.sectionTitle || 'Main Content';

    for (let i = 0; i < sentences.length; i++) {
      const sentence = sentences[i].trim();
      
      // Detect potential section header
      if (sentence.length < 80 && (sentence.startsWith('Section') || sentence.startsWith('Chapter') || sentence.includes(':') || /^[0-9]+(\.[0-9]+)*/.test(sentence))) {
        currentSection = sentence;
      }

      if ((currentChunkText + ' ' + sentence).length <= chunkSize || currentChunkText.length === 0) {
        currentChunkText = currentChunkText ? currentChunkText + ' ' + sentence : sentence;
      } else {
        // Finalize chunk
        if (currentChunkText.trim().length > 0) {
          chunks.push(createChunkObject({
            chunkIndex: chunkIndex++,
            pageNumber: pageNum,
            sectionTitle: currentSection,
            content: currentChunkText.trim(),
            metadata
          }));
        }

        // Overlap management
        const words = currentChunkText.split(' ');
        const overlapWords = words.slice(-Math.min(words.length, Math.floor(chunkOverlap / 6)));
        currentChunkText = overlapWords.join(' ') + ' ' + sentence;
      }
    }

    // Flush remaining text on page
    if (currentChunkText.trim().length > 0) {
      chunks.push(createChunkObject({
        chunkIndex: chunkIndex++,
        pageNumber: pageNum,
        sectionTitle: currentSection,
        content: currentChunkText.trim(),
        metadata
      }));
    }
  }

  return chunks;
}

function createChunkObject({ chunkIndex, pageNumber, sectionTitle, content, metadata }) {
  const tokenCount = Math.ceil(content.split(/\s+/).length * 1.3);
  const hashId = crypto.createHash('md5').update(`${metadata.versionId}_chunk_${chunkIndex}_${content.substring(0, 30)}`).digest('hex');

  return {
    id: `chunk_${hashId}`,
    version_id: metadata.versionId,
    document_id: metadata.documentId,
    group_id: metadata.groupId,
    document_title: metadata.documentTitle || 'Untitled Document',
    version_number: metadata.versionNumber || '1.0',
    chunk_index: chunkIndex,
    page_number: pageNumber,
    section_title: sectionTitle,
    content: content,
    token_count: tokenCount,
    status: metadata.status || 'Draft',
    effective_date: metadata.effectiveDate || null,
    expiration_date: metadata.expirationDate || null,
    created_at: new Date().toISOString()
  };
}
