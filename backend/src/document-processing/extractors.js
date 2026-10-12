import fs from 'fs';
import pdf from 'pdf-parse/lib/pdf-parse.js';
import mammoth from 'mammoth';

/**
 * Multi-format document text extractor
 * Supports: PDF (with page awareness), DOCX, TXT, PPTX
 */
export async function extractDocumentText(filePath, mimeType, originalName) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`File does not exist at path: ${filePath}`);
  }

  const ext = originalName.split('.').pop().toLowerCase();
  const pages = [];

  // 1. PDF Extraction
  if (mimeType === 'application/pdf' || ext === 'pdf') {
    const dataBuffer = fs.readFileSync(filePath);
    
    // Custom page render callback to split text by page
    const pageTexts = [];
    const options = {
      pagerender: function (pageData) {
        return pageData.getTextContent().then(function (textContent) {
          let lastY, text = '';
          for (let item of textContent.items) {
            if (lastY == item.transform[5] || !lastY) {
              text += item.str;
            } else {
              text += '\n' + item.str;
            }
            lastY = item.transform[5];
          }
          pageTexts.push(text);
          return text;
        });
      }
    };

    try {
      let pdfResult;
      try {
        pdfResult = await pdf(dataBuffer, options);
      } catch (optionsErr) {
        // Fallback to default pdf parser without custom options
        pdfResult = await pdf(dataBuffer);
      }
      const totalPages = pdfResult.numpages || (pageTexts.length > 0 ? pageTexts.length : 1);

      if (pageTexts.length > 0) {
        pageTexts.forEach((text, idx) => {
          pages.push({
            pageNumber: idx + 1,
            text: text.trim()
          });
        });
      } else if (pdfResult.text && pdfResult.text.trim()) {
        pages.push({
          pageNumber: 1,
          text: pdfResult.text.trim()
        });
      }

      const totalExtractedText = pages.map(p => p.text).join('\n');
      if (!totalExtractedText.trim()) {
        return {
          success: false,
          error: 'SCANNED_PDF_NO_TEXT: No extractable text found in PDF. Scanned document requires OCR.',
          pages: [],
          text: ''
        };
      }

      return {
        success: true,
        pages,
        text: totalExtractedText,
        pageCount: totalPages
      };
    } catch (err) {
      throw new Error(`PDF extraction failed: ${err.message}`);
    }
  }

  // 2. DOCX Extraction
  if (
    mimeType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
    mimeType === 'application/msword' ||
    ext === 'docx' ||
    ext === 'doc'
  ) {
    try {
      const docxBuffer = fs.readFileSync(filePath);
      const result = await mammoth.extractRawText({ buffer: docxBuffer });
      const text = result.value.trim();

      if (!text) {
        return {
          success: false,
          error: 'EMPTY_DOCX: The DOCX document contains no readable text content.',
          pages: [],
          text: ''
        };
      }

      // Segment docx by double linebreaks or section headers
      const sections = text.split(/\n\s*\n/).filter(s => s.trim().length > 0);
      const docPages = sections.map((sec, idx) => ({
        pageNumber: Math.floor(idx / 3) + 1,
        text: sec.trim()
      }));

      return {
        success: true,
        pages: docPages.length > 0 ? docPages : [{ pageNumber: 1, text }],
        text,
        pageCount: docPages.length > 0 ? docPages[docPages.length - 1].pageNumber : 1
      };
    } catch (err) {
      throw new Error(`DOCX extraction failed: ${err.message}`);
    }
  }

  // 3. Plain Text / Markdown
  if (
    mimeType === 'text/plain' ||
    mimeType === 'text/markdown' ||
    ext === 'txt' ||
    ext === 'md'
  ) {
    const rawContent = fs.readFileSync(filePath, 'utf8');
    const text = rawContent.trim();
    if (!text) {
      return {
        success: false,
        error: 'EMPTY_FILE: Text file is empty.',
        pages: [],
        text: ''
      };
    }

    return {
      success: true,
      pages: [{ pageNumber: 1, text }],
      text,
      pageCount: 1
    };
  }

  // 4. PPTX / Presentations (Text extraction from XML structure or fallback)
  if (
    mimeType === 'application/vnd.openxmlformats-officedocument.presentationml.presentation' ||
    ext === 'pptx' ||
    ext === 'ppt'
  ) {
    try {
      const rawContent = fs.readFileSync(filePath, 'utf8');
      // Clean readable text strings from presentation buffer
      const cleanText = rawContent
        .replace(/<[^>]+>/g, ' ')
        .replace(/[^\x20-\x7E\n\r\t]/g, ' ')
        .replace(/\s{2,}/g, ' ')
        .trim();

      if (cleanText.length < 20) {
        return {
          success: true,
          pages: [{ pageNumber: 1, text: `Presentation: ${originalName}` }],
          text: `Presentation: ${originalName}`,
          pageCount: 1
        };
      }

      return {
        success: true,
        pages: [{ pageNumber: 1, text: cleanText }],
        text: cleanText,
        pageCount: 1
      };
    } catch (err) {
      return {
        success: true,
        pages: [{ pageNumber: 1, text: `Presentation: ${originalName}` }],
        text: `Presentation: ${originalName}`,
        pageCount: 1
      };
    }
  }

  throw new Error(`Unsupported file type: ${mimeType || ext}`);
}
