/**
 * Version Validation & Eligibility Engine
 * Enforces strict temporal, status, and lineage rules for RAG
 */

export const versionRules = {
  /**
   * Determine query mode: 'CURRENT' | 'HISTORICAL' | 'COMPARISON'
   */
  classifyQueryIntent(query) {
    const qLower = query.toLowerCase();

    // 1. Comparison Intent
    if (
      qLower.includes('compare') ||
      qLower.includes('difference between') ||
      qLower.includes('what changed between') ||
      qLower.includes('versus') ||
      (qLower.includes('version') && (qLower.includes(' and ') || qLower.includes(' to ')))
    ) {
      // Extract target version tags if present
      const verMatches = qLower.match(/version\s*([0-9\.]+)|v([0-9\.]+)/g) || [];
      return {
        intent: 'COMPARISON',
        targetVersions: verMatches.map(v => v.replace(/version\s*|v/i, ''))
      };
    }

    // 2. Historical Intent
    if (
      qLower.includes('in 202') ||
      qLower.includes('in 201') ||
      qLower.includes('historical') ||
      qLower.includes('previous') ||
      qLower.includes('old version') ||
      qLower.includes('prior to') ||
      qLower.includes('in version') ||
      qLower.includes('under version') ||
      qLower.includes('stated in v')
    ) {
      const verMatch = qLower.match(/version\s*([0-9\.]+)|v([0-9\.]+)/i);
      const yearMatch = qLower.match(/\b(20[12][0-9])\b/);
      return {
        intent: 'HISTORICAL',
        targetVersion: verMatch ? (verMatch[1] || verMatch[2]) : null,
        targetYear: yearMatch ? yearMatch[1] : null
      };
    }

    // 3. Default: Current-Version Intent
    return {
      intent: 'CURRENT'
    };
  },

  /**
   * Filter versions according to intent and temporal rules
   */
  resolveEligibleVersions(allVersions, intentInfo) {
    if (!allVersions || allVersions.length === 0) {
      return {
        eligibleVersions: [],
        conflictWarning: null,
        statusNote: 'No document versions available in repository.'
      };
    }

    const { intent, targetVersion, targetYear, targetVersions } = intentInfo;

    // Group versions by document_id / group_id
    const groups = {};
    for (const v of allVersions) {
      const gId = v.group_id || v.document_id;
      if (!groups[gId]) groups[gId] = [];
      groups[gId].push(v);
    }

    const eligible = [];
    let conflictWarning = null;

    // Process each document family
    for (const [groupId, versions] of Object.entries(groups)) {
      
      // CASE 1: Current-Version Query
      if (intent === 'CURRENT') {
        const activeVers = versions.filter(v => v.status === 'Active');

        // Check for multiple conflicting active versions
        if (activeVers.length > 1) {
          conflictWarning = `⚠️ CONFLICT DETECTED: Document family has multiple active versions (${activeVers.map(v => 'v' + v.version_number).join(', ')}). The system cannot silently select one without administrative resolution.`;
          eligible.push(...activeVers); // Retrieve from both to highlight the conflict
          continue;
        }

        if (activeVers.length === 1) {
          const active = activeVers[0];
          // Check expiration
          if (active.expiration_date && new Date(active.expiration_date) < new Date()) {
            conflictWarning = `⚠️ ACTIVE VERSION EXPIRED: Version v${active.version_number} was marked Active but expired on ${active.expiration_date}.`;
          }
          eligible.push(active);
        } else {
          // No version explicitly marked 'Active'
          const nonSuperseded = versions.filter(v => v.status !== 'Superseded' && v.status !== 'Archived' && v.status !== 'Expired');
          if (nonSuperseded.length > 0) {
            eligible.push(nonSuperseded[0]);
          }
        }
      }

      // CASE 2: Historical Query
      else if (intent === 'HISTORICAL') {
        if (targetVersion) {
          const match = versions.find(v => v.version_number.toString() === targetVersion);
          if (match) {
            eligible.push(match);
          } else {
            // Include all historical versions for evaluation
            eligible.push(...versions.filter(v => v.status === 'Superseded' || v.status === 'Archived'));
          }
        } else if (targetYear) {
          const yearMatch = versions.filter(v => (v.effective_date && v.effective_date.includes(targetYear)) || (v.uploaded_at && v.uploaded_at.includes(targetYear)));
          if (yearMatch.length > 0) {
            eligible.push(...yearMatch);
          } else {
            eligible.push(...versions);
          }
        } else {
          eligible.push(...versions);
        }
      }

      // CASE 3: Comparison Query
      else if (intent === 'COMPARISON') {
        if (targetVersions && targetVersions.length >= 2) {
          const matches = versions.filter(v => targetVersions.includes(v.version_number.toString()));
          eligible.push(...matches);
        } else {
          // Compare active with latest superseded
          eligible.push(...versions.slice(0, 3));
        }
      }
    }

    return {
      eligibleVersions: eligible,
      conflictWarning,
      statusNote: `Resolved ${eligible.length} eligible version(s) for query intent: ${intent}`
    };
  }
};
