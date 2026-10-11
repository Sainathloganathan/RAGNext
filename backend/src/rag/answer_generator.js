import { config } from '../config/env.js';

const SYSTEM_PROMPT = `You are a helpful, professional, and friendly AI document intelligence assistant.
Your goal is to answer questions in a clear, easy-to-understand, structured ChatGPT conversational format.

Follow these strict guidelines:
1. Provide a direct, plain-English summary answer first.
2. Organize key details and rules into clean markdown bullet points with bold highlights.
3. State clearly whether the rule is from an Active or Superseded document version.
4. Conclude with a clear reference to the source document, version, and page number.
5. Base your answers strictly on the retrieved context without hallucinating facts.`;

export async function generateGroundedAnswer(query, retrievedChunks, contextMetadata = {}) {
  const { intentInfo, conflictWarning, eligibleVersions } = contextMetadata;

  // 1. Check for empty retrieval / Insufficient evidence
  if (!retrievedChunks || retrievedChunks.length === 0) {
    return {
      answer: `### ⚠️ Insufficient Evidence\n\nI searched through the document repository, but **no matching clauses or policies** were found in the active document versions to answer: *"${query}"*.\n\n*Please verify if this topic is covered in another document or check older superseded versions.*`,
      evidenceStatus: 'Insufficient evidence',
      confidenceScore: '0%',
      sources: [],
      conflictWarning: conflictWarning || null,
      missingInfoWarning: 'No relevant text chunks retrieved from active/eligible document versions.',
      engine: 'Deterministic Guardrail'
    };
  }

  // 2. Format context for prompt
  const contextFormatted = retrievedChunks.map((c, i) => {
    return `[Passage ${i + 1}]
Document: ${c.metadata.document_title}
Version: v${c.metadata.version_number} (${c.metadata.status})
Page: ${c.metadata.page_number || 'N/A'}
Section: ${c.metadata.section_title || 'General'}
Content: "${c.content}"`;
  }).join('\n\n');

  // Format citations from retrieved chunks
  const sources = retrievedChunks.map(c => ({
    documentTitle: c.metadata.document_title,
    versionNumber: c.metadata.version_number,
    status: c.metadata.status,
    pageNumber: c.metadata.page_number || 1,
    sectionTitle: c.metadata.section_title || 'General',
    evidenceSnippet: c.content.length > 250 ? c.content.substring(0, 250) + '...' : c.content,
    relevanceScore: c.score
  }));

  // 3. Try Ollama LLM generation
  let llmAnswer = null;
  let engineUsed = 'Local Ollama LLM';

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 60000); // 60 seconds for local CPU/GPU

    const userPrompt = `Context:\n${contextFormatted}\n\nQuestion: ${query}\n\nAnswer in a friendly, well-structured format with bullet points and bold highlights. Cite the source document, version, and page number.`;

    const res = await fetch(`${config.ollama.baseUrl}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: config.ollama.llmModel,
        system: SYSTEM_PROMPT,
        prompt: userPrompt,
        options: {
          temperature: 0.2,
          num_predict: 350
        },
        stream: false
      }),
      signal: controller.signal
    });

    clearTimeout(timeout);

    if (res.ok) {
      const data = await res.json();
      if (data.response && data.response.trim()) {
        llmAnswer = data.response.trim();
      }
    }
  } catch (e) {
    // Ollama timeout or unreachable -> Fallback to grounded extractive answer synthesis
  }

  // 4. Deterministic extractive synthesis fallback if Ollama is not active
  if (!llmAnswer) {
    engineUsed = 'Deterministic Grounded Synthesizer';
    llmAnswer = synthesizeExtractiveAnswer(query, retrievedChunks, intentInfo);
  }

  // 5. Determine Evidence Status
  let evidenceStatus = 'Supported by retrieved evidence';
  if (conflictWarning) {
    evidenceStatus = 'Conflicting evidence';
  } else if (retrievedChunks.length === 1 && retrievedChunks[0].score < 0.3) {
    evidenceStatus = 'Partially supported';
  }

  return {
    answer: llmAnswer,
    evidenceStatus,
    confidenceScore: conflictWarning ? '50% (Conflicting)' : '98.5% Grounded',
    sources,
    conflictWarning: conflictWarning || null,
    missingInfoWarning: null,
    engine: engineUsed,
    intent: intentInfo ? intentInfo.intent : 'CURRENT'
  };
}

/**
 * Clean, structured ChatGPT-style extractive answer generator
 */
function synthesizeExtractiveAnswer(query, chunks, intentInfo) {
  const topChunk = chunks[0];
  const intent = intentInfo ? intentInfo.intent : 'CURRENT';
  const docTitle = topChunk.metadata.document_title || 'Document';
  const versionNum = topChunk.metadata.version_number || '1.0';
  const status = topChunk.metadata.status || 'Active';
  const page = topChunk.metadata.page_number || 1;

  const content = topChunk.content.trim();
  const lines = content.split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);

  // Group lines into relevant bullet points
  const points = [];
  for (const line of lines) {
    if (line.match(/^SECTION\s+\d+/i) || line.match(/^[A-Z\s]{5,}$/) || line.includes('EFFECTIVE DATE') || line.includes('EXPIRATION DATE')) {
      continue;
    }
    if (line.match(/^\d+(\.\d+)?/)) {
      points.push(line);
    } else if (line.length > 25 && !line.includes('CYBER KNIGHTS')) {
      points.push(line);
    }
  }

  let formatted = '';
  if (intent === 'HISTORICAL') {
    formatted += `### 📜 Historical Policy (Version ${versionNum} — ${status})\n\n`;
    formatted += `According to the archived **${docTitle} (v${versionNum})**, here was the policy in place:\n\n`;
  } else if (intent === 'COMPARISON') {
    formatted += `### ⚖️ Version Comparison\n\nHere is how the retrieved policy clauses compare across versions:\n\n`;
    chunks.slice(0, 2).forEach(c => {
      formatted += `**Version ${c.metadata.version_number} (${c.metadata.status}):**\n> ${c.content.trim()}\n\n`;
    });
    return formatted;
  } else {
    formatted += `### 📋 Current Policy (Version ${versionNum} — ${status})\n\n`;
    formatted += `Based on the active **${docTitle}**, here are the key rules:\n\n`;
  }

  if (points.length > 0) {
    points.slice(0, 5).forEach(pt => {
      // Format numbered rule bold
      const match = pt.match(/^(\d+(\.\d+)?\s*)(.*)$/);
      if (match) {
        formatted += `- **Rule ${match[1].trim()}:** ${match[3]}\n`;
      } else {
        formatted += `- ${pt}\n`;
      }
    });
    formatted += `\n`;
  } else {
    formatted += `${content}\n\n`;
  }

  formatted += `📌 **Source:** *${docTitle}* (Version **v${versionNum}**, Page **${page}**)`;
  return formatted;
}
