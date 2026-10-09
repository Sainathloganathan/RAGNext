/**
 * RAGNext — Edutorial Interactive Engine
 * Controls Sandbox simulations, Workflow Stepper, Dual Engine Switcher, ROI math & Pitch Deck
 */

document.addEventListener('DOMContentLoaded', () => {

  /* --------------------------------------------------------------------------
     1. HERO DUAL ENGINE TOGGLE & PRESET CHIPS
     -------------------------------------------------------------------------- */
  const toggleRagNext = document.getElementById('toggleRagNext');
  const toggleLegacy = document.getElementById('toggleLegacy');
  const heroRagNextView = document.getElementById('heroRagNextView');
  const heroLegacyView = document.getElementById('heroLegacyView');
  const heroQueryText = document.getElementById('heroQueryText');
  const heroPromptChips = document.querySelectorAll('.hero-prompt-suggestions .chip-prompt');

  if (toggleRagNext && toggleLegacy) {
    toggleRagNext.addEventListener('click', () => {
      toggleRagNext.classList.add('active');
      toggleLegacy.classList.remove('active');
      heroRagNextView.style.display = 'block';
      heroLegacyView.style.display = 'none';
    });

    toggleLegacy.addEventListener('click', () => {
      toggleLegacy.classList.add('active');
      toggleRagNext.classList.remove('active');
      heroRagNextView.style.display = 'none';
      heroLegacyView.style.display = 'block';
    });
  }

  heroPromptChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const q = chip.dataset.query;
      if (q === 'hydraulic') {
        heroQueryText.textContent = '"What is the maximum permissible pressure for Hydraulic Press Model X-400 in 2025?"';
        heroRagNextView.querySelector('.answer-text').innerHTML = 'Under the latest <strong>Machinery Safety Bulletin v2.4 (2025)</strong>, the maximum continuous pressure is strictly capped at <strong>350 bar</strong>. The older 450 bar rating from v1.2 has been deprecated due to valve stress fatigue advisories.';
        heroRagNextView.querySelector('.evidence-pill:nth-child(1) .pill-v').textContent = 'Hydraulic_Press_Manual_v2.4.pdf';
        heroRagNextView.querySelector('.evidence-pill:nth-child(2) .pill-v').textContent = 'v2.4 (Valid)';
        heroRagNextView.querySelector('.evidence-pill:nth-child(3) .pill-v').textContent = 'Page 42, §3.8';
        
        heroLegacyView.querySelector('.answer-text').innerHTML = 'Maximum permissible operating pressure is rated at <strong>450 bar</strong> continuously.';
        heroLegacyView.querySelector('.evidence-pill:nth-child(1) .pill-v').textContent = 'Press_Manual_2019_v1.2.pdf';
        heroLegacyView.querySelector('.evidence-pill:nth-child(2) .pill-v').textContent = 'v1.2 (Expired)';
      } else if (q === 'clinical') {
        heroQueryText.textContent = '"What is the initial antibiotic protocol for adult sepsis triage in the ER?"';
        heroRagNextView.querySelector('.answer-text').innerHTML = 'According to the <strong>2024 Clinical Sepsis Guideline (v3.1)</strong>, administer <strong>IV Broad-Spectrum Ceftriaxone 2g within 45 minutes</strong> of lactate elevation. Ampicillin monotherapy from 2020 protocol is no longer first-line.';
        heroRagNextView.querySelector('.evidence-pill:nth-child(1) .pill-v').textContent = 'Clinical_Sepsis_SOP_v3.1.pdf';
        heroRagNextView.querySelector('.evidence-pill:nth-child(2) .pill-v').textContent = 'v3.1 (Valid)';
        heroRagNextView.querySelector('.evidence-pill:nth-child(3) .pill-v').textContent = 'Page 09, §2.1';
        
        heroLegacyView.querySelector('.answer-text').innerHTML = 'Administer Ampicillin 1000mg IV within 3 hours of patient intake.';
        heroLegacyView.querySelector('.evidence-pill:nth-child(1) .pill-v').textContent = 'Sepsis_Guideline_2020_v1.0.pdf';
        heroLegacyView.querySelector('.evidence-pill:nth-child(2) .pill-v').textContent = 'v1.0 (Expired)';
      }
    });
  });

  /* --------------------------------------------------------------------------
     2. 6-STAGE WORKFLOW STEPPER CONTROLS
     -------------------------------------------------------------------------- */
  const stepButtons = document.querySelectorAll('.step-nav-btn');
  const stepPanes = document.querySelectorAll('.workflow-step-pane');
  const btnPrevStep = document.getElementById('btnPrevStep');
  const btnNextStep = document.getElementById('btnNextStep');
  const stepIndicatorText = document.getElementById('stepIndicatorText');
  const btnAutoPlay = document.getElementById('btnAutoPlayWorkflow');
  const autoPlayText = document.getElementById('autoPlayText');

  let currentStep = 1;
  const totalSteps = 6;
  let autoPlayTimer = null;

  const stepTitles = [
    'Input Documents',
    'Read & Understand Documents',
    'Store with Version Lineage',
    'User Question Formulation',
    'Find Latest Version & Retrieve',
    'Structured Output & Source Evidence'
  ];

  function setStep(stepNum) {
    currentStep = stepNum;
    stepButtons.forEach(btn => {
      const bStep = parseInt(btn.dataset.step, 10);
      btn.classList.toggle('active', bStep === currentStep);
    });

    stepPanes.forEach(pane => {
      const pStep = parseInt(pane.dataset.step, 10);
      pane.classList.toggle('active', pStep === currentStep);
    });

    if (stepIndicatorText) {
      stepIndicatorText.textContent = `Showing Step ${currentStep} of ${totalSteps}: ${stepTitles[currentStep - 1]}`;
    }

    if (btnPrevStep) {
      btnPrevStep.disabled = currentStep === 1;
    }
    if (btnNextStep) {
      btnNextStep.disabled = currentStep === totalSteps;
      btnNextStep.classList.toggle('active', currentStep < totalSteps);
    }
  }

  stepButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      stopAutoPlay();
      setStep(parseInt(btn.dataset.step, 10));
    });
  });

  if (btnPrevStep) {
    btnPrevStep.addEventListener('click', () => {
      stopAutoPlay();
      if (currentStep > 1) setStep(currentStep - 1);
    });
  }

  if (btnNextStep) {
    btnNextStep.addEventListener('click', () => {
      stopAutoPlay();
      if (currentStep < totalSteps) setStep(currentStep + 1);
    });
  }

  function stopAutoPlay() {
    if (autoPlayTimer) {
      clearInterval(autoPlayTimer);
      autoPlayTimer = null;
      if (autoPlayText) autoPlayText.textContent = 'Auto-Play Tour';
    }
  }

  if (btnAutoPlay) {
    btnAutoPlay.addEventListener('click', () => {
      if (autoPlayTimer) {
        stopAutoPlay();
      } else {
        if (autoPlayText) autoPlayText.textContent = 'Pause Tour';
        autoPlayTimer = setInterval(() => {
          let next = currentStep + 1;
          if (next > totalSteps) next = 1;
          setStep(next);
        }, 3200);
      }
    });
  }

  /* --------------------------------------------------------------------------
     3. LIVE SANDBOX DATA & INTERACTION (SLIDE 2 & 3 SIMULATION)
     -------------------------------------------------------------------------- */
  const scenarioData = {
    hr: {
      name: 'Corporate HR Policies & Employee Handbooks',
      activeVersion: 'v3.0 (Jan 2025 Edition)',
      queries: [
        'What is the daily maximum allowance for meals during business travel?',
        'How many days of paid parental leave are allocated for primary caregivers in 2025?',
        'Can remote home office equipment be expensed without prior director sign-off?'
      ],
      defaultQuery: 'What is the daily maximum allowance for meals and hotel during overseas trips?',
      answer: 'Under the active <strong>2025 Global Travel & Expense Policy (v3.0)</strong>, the daily meal per diem has been revised to <strong>$85 USD / day</strong> (up from $60 in v2.0), and the maximum hotel accommodation allowance is <strong>$280 USD / night for Tier-1 cities</strong> and <strong>$210 USD / night for Tier-2 cities</strong>. Alcohol expenses remain non-reimbursable unless part of an authorized client entertainment dinner.',
      source: 'Global_HR_Policy_Manual_2025.pdf',
      version: 'v3.0 (Supersedes v1.0 & v2.0)',
      page: 'Page 18, Section 4.2.1',
      grounding: '99.8% (0% Hallucination)',
      lineage: ['v1.0 (2021) ❌', 'v2.0 (2023) ❌', 'v3.0 (2025) ✔ Active'],
      evidenceBadge: 'Page 18 Snippet',
      evidenceExcerpt: '"...[Section 4.2.1 Meal & Lodging Allowances] Commencing January 1, 2025, employees traveling internationally are eligible for <mark class=\'doc-highlight\'>a daily meal per diem of $85 USD</mark>. Hotel lodging reimbursements are capped at <mark class=\'doc-highlight\'>$280 USD per night in Tier 1 metropolises</mark> (London, Tokyo, New York, Singapore) and $210 USD per night in Tier 2 regions. This document supersedes all previous editions including Policy Memo 2023-08 (v2.0)..."'
    },
    engineering: {
      name: 'Machinery SOPs & Industrial Safety Specs',
      activeVersion: 'v2.4 (Safety Bulletin 2025 Active)',
      queries: [
        'What is the continuous operating pressure threshold for Hydraulic Press 400?',
        'What is the mandatory calibration frequency for emergency pressure valves?',
        'What torque specification is required on flange bolts during re-assembly?'
      ],
      defaultQuery: 'What is the continuous operating pressure threshold for Hydraulic Press 400?',
      answer: 'According to the updated <strong>Hydraulic Press Safety SOP (v2.4)</strong>, continuous operating pressure must never exceed <strong>350 bar</strong>. The previous v1.2 specification of 450 bar was revoked after thermal valve fatigue testing. Operators must conduct daily zero-point sensor checks.',
      source: 'Machinery_SOP_Press_v2.4.pdf',
      version: 'v2.4 (Supersedes v1.2)',
      page: 'Page 42, §3.8.2',
      grounding: '100% Verifiable',
      lineage: ['v1.2 (2019) ❌', 'v2.0 (2022) ❌', 'v2.4 (2025) ✔ Active'],
      evidenceBadge: 'Page 42 Snippet',
      evidenceExcerpt: '"...[Section 3.8.2 Pressure Limit Override Alert] CAUTION: Under Engineering Directive 2024-B, <mark class=\'doc-highlight\'>maximum continuous hydraulic pressure is reduced from 450 bar to 350 bar</mark> across all Mark-IV units. Exceeding 350 bar triggers emergency automatic solenoid dump..."'
    },
    healthcare: {
      name: 'Clinical Sepsis Guidelines & Hospital SOPs',
      activeVersion: '2024 WHO/FDA Clinical Standard (v3.1)',
      queries: [
        'What is the first-line intravenous antibiotic regimen for septic shock intake?',
        'Within what timeframe must lactate re-evaluation occur after fluid resuscitation?',
        'What is the dosing threshold for noradrenaline infusion in refractory hypotension?'
      ],
      defaultQuery: 'What is the first-line intravenous antibiotic regimen for septic shock intake?',
      answer: 'Per the revised <strong>Clinical Sepsis Guideline (v3.1, 2024 Edition)</strong>, first-line treatment requires <strong>Ceftriaxone 2g IV + Vancomycin 15mg/kg</strong> administered strictly within <strong>45 minutes of triage confirmation</strong>. Monotherapy protocols from 2020 are discontinued.',
      source: 'Clinical_Sepsis_Guideline_v3.1.pdf',
      version: 'v3.1 (Supersedes 2020 v1.0)',
      page: 'Page 09, Table 2.4',
      grounding: '99.9% Clinical Confidence',
      lineage: ['v1.0 (2020) ❌', 'v2.0 (2022) ❌', 'v3.1 (2024) ✔ Active'],
      evidenceBadge: 'Page 09 Snippet',
      evidenceExcerpt: '"...[Table 2.4 Empirical Antimicrobial Therapy] For patients presenting with lactate > 4.0 mmol/L, initiate <mark class=\'doc-highlight\'>IV Ceftriaxone 2g + Vancomycin within 45 mins</mark>. The 2020 3-hour window protocol is hereby repealed per International Sepsis Consensus 2024..."'
    },
    finance: {
      name: 'Corporate Tax & AML Compliance Directives',
      activeVersion: 'FY2025 Regulatory Circular (v4.0)',
      queries: [
        'What is the mandatory dollar threshold for filing Suspicious Activity Reports (SAR)?',
        'What is the depreciation rate for enterprise cloud AI server capital expenditure?',
        'Are cross-border consulting payments subject to withholding tax under Section 195?'
      ],
      defaultQuery: 'What is the mandatory dollar threshold for filing Suspicious Activity Reports (SAR)?',
      answer: 'Under <strong>Circular No. 14/FY25 (v4.0)</strong>, any single or aggregated transaction exceeding <strong>$10,000 USD (or equivalent)</strong> with high-risk jurisdiction flags requires an automated <strong>Suspicious Transaction Report (STR/SAR)</strong> filed within <strong>24 business hours</strong> (shortened from 72h in FY22).',
      source: 'AML_Compliance_Directive_FY25.pdf',
      version: 'v4.0 (Supersedes FY22 & FY24)',
      page: 'Page 27, Clause 6.1',
      grounding: '100% Audit Ready',
      lineage: ['FY22 (v1.0) ❌', 'FY24 (v2.0) ❌', 'FY25 (v4.0) ✔ Active'],
      evidenceBadge: 'Page 27 Snippet',
      evidenceExcerpt: '"...[Clause 6.1 Mandatory Thresholds] In compliance with FATF 2025 directives, <mark class=\'doc-highlight\'>the transaction reporting threshold is fixed at $10,000 USD</mark> with mandatory filing mandated within 24 hours of algorithmic flag trigger..."'
    }
  };

  let activeScenarioKey = 'hr';

  const scenarioButtons = document.querySelectorAll('.scenario-btn');
  const activeScenarioName = document.getElementById('activeScenarioName');
  const activeVersionPill = document.getElementById('activeVersionPill');
  const sandboxQueryInput = document.getElementById('sandboxQueryInput');
  const sampleQueriesBar = document.getElementById('sampleQueriesBar');
  const btnExecuteQuery = document.getElementById('btnExecuteQuery');

  const resAnswerParagraph = document.getElementById('resAnswerParagraph');
  const resMetaSource = document.getElementById('resMetaSource');
  const resMetaVersion = document.getElementById('resMetaVersion');
  const resMetaPage = document.getElementById('resMetaPage');
  const resMetaGrounding = document.getElementById('resMetaGrounding');
  const resVersionLineage = document.getElementById('resVersionLineage');
  const resEvidenceBadge = document.getElementById('resEvidenceBadge');
  const resEvidenceContent = document.getElementById('resEvidenceContent');
  const resLatencyTag = document.getElementById('resLatencyTag');

  function renderScenario(key) {
    activeScenarioKey = key;
    const data = scenarioData[key];
    if (!data) return;

    scenarioButtons.forEach(b => b.classList.toggle('active', b.dataset.scenario === key));

    if (activeScenarioName) activeScenarioName.textContent = data.name;
    if (activeVersionPill) {
      activeVersionPill.innerHTML = `<span class="dot-green"></span><span>Active Truth: <strong>${data.activeVersion}</strong></span>`;
    }

    if (sandboxQueryInput) sandboxQueryInput.value = data.defaultQuery;

    // Render Query Chips
    if (sampleQueriesBar) {
      sampleQueriesBar.innerHTML = '';
      data.queries.forEach(q => {
        const chip = document.createElement('button');
        chip.className = 'sample-query-chip';
        chip.textContent = q;
        chip.addEventListener('click', () => {
          sandboxQueryInput.value = q;
          runSimulation();
        });
        sampleQueriesBar.appendChild(chip);
      });
    }

    renderResults(data);
  }

  function renderResults(data) {
    if (resAnswerParagraph) resAnswerParagraph.innerHTML = data.answer;
    if (resMetaSource) resMetaSource.textContent = data.source;
    if (resMetaVersion) resMetaVersion.textContent = data.version;
    if (resMetaPage) resMetaPage.textContent = data.page;
    if (resMetaGrounding) resMetaGrounding.textContent = data.grounding;
    if (resEvidenceBadge) resEvidenceBadge.textContent = data.evidenceBadge;
    if (resEvidenceContent) resEvidenceContent.innerHTML = data.evidenceExcerpt;

    if (resVersionLineage) {
      resVersionLineage.innerHTML = data.lineage.map(l => {
        const isCurrent = l.includes('Active');
        return `<span class="chip-v ${isCurrent ? 'current' : 'old'}">${l}</span>`;
      }).join('');
    }
  }

  function runSimulation() {
    const data = scenarioData[activeScenarioKey];
    if (!data) return;

    if (btnExecuteQuery) {
      btnExecuteQuery.innerHTML = `<span>Resolving Lineage...</span>`;
      btnExecuteQuery.style.opacity = '0.7';
    }

    if (resAnswerParagraph) {
      resAnswerParagraph.innerHTML = `<span style="color: #64748B;">Scanning temporal document graph and eliminating superseded chunks...</span>`;
    }

    const randomLatency = Math.floor(Math.random() * 200) + 520;

    setTimeout(() => {
      if (resLatencyTag) resLatencyTag.textContent = `Response generated in ${randomLatency}ms`;
      renderResults(data);
      if (btnExecuteQuery) {
        btnExecuteQuery.innerHTML = `<span>Run Version-Aware RAG</span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;
        btnExecuteQuery.style.opacity = '1';
      }
    }, 450);
  }

  scenarioButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      renderScenario(btn.dataset.scenario);
    });
  });

  if (btnExecuteQuery) {
    btnExecuteQuery.addEventListener('click', () => {
      runSimulation();
    });
  }

  // Simulated Upload Button
  const btnSimUpload = document.getElementById('btnSimUploadNewVersion');
  if (btnSimUpload) {
    btnSimUpload.addEventListener('click', () => {
      const fileName = `Revision_${activeScenarioKey.toUpperCase()}_v4.0_2026.pdf`;
      alert(`[RAGNext Ingestion Gateway]\nSuccessfully parsed: ${fileName}\nTemporal Tag: v4.0 (Live Active)\nPrevious v3.0 automatically marked as historical archive.`);
      const data = scenarioData[activeScenarioKey];
      if (data) {
        data.lineage.push('v4.0 (2026) ✔ Active');
        data.lineage = data.lineage.map(item => item.includes('v3.0') ? item.replace('✔ Active', '❌ Superseded') : item);
        renderScenario(activeScenarioKey);
      }
    });
  }

  // Initialize Default Scenario
  renderScenario('hr');

  /* --------------------------------------------------------------------------
     4. ROI & PRODUCTIVITY CALCULATOR (CHAPTER 06)
     -------------------------------------------------------------------------- */
  const inputTeam = document.getElementById('inputTeamSize');
  const inputHours = document.getElementById('inputSearchHours');
  const inputRate = document.getElementById('inputHourlyRate');
  const inputRevisions = document.getElementById('inputRevisionCount');

  const valDisplayTeam = document.getElementById('valDisplayTeam');
  const valDisplayHours = document.getElementById('valDisplayHours');
  const valDisplayRate = document.getElementById('valDisplayRate');
  const valDisplayRevisions = document.getElementById('valDisplayRevisions');

  const metricAnnualSavings = document.getElementById('metricAnnualSavings');
  const metricHoursSaved = document.getElementById('metricHoursSaved');
  const metricRiskReduced = document.getElementById('metricRiskReduced');

  function calculateROI() {
    if (!inputTeam || !inputHours || !inputRate) return;

    const team = parseInt(inputTeam.value, 10);
    const hoursPerWeek = parseFloat(inputHours.value);
    const hourlyRate = parseFloat(inputRate.value);
    const revisions = parseInt(inputRevisions ? inputRevisions.value : '15', 10);

    if (valDisplayTeam) valDisplayTeam.textContent = `${team.toLocaleString()} people`;
    if (valDisplayHours) valDisplayHours.textContent = `${hoursPerWeek.toFixed(1)} hrs`;
    if (valDisplayRate) valDisplayRate.textContent = `$${hourlyRate} / hr`;
    if (valDisplayRevisions) valDisplayRevisions.textContent = `${revisions} revisions`;

    // 52 work weeks, 80% time recovery efficiency with RAGNext
    const totalHoursSpentYear = team * hoursPerWeek * 50;
    const hoursSavedYear = Math.round(totalHoursSpentYear * 0.80);
    const dollarsSavedYear = Math.round(hoursSavedYear * hourlyRate);

    if (metricAnnualSavings) metricAnnualSavings.textContent = `$${dollarsSavedYear.toLocaleString()}`;
    if (metricHoursSaved) metricHoursSaved.textContent = `${hoursSavedYear.toLocaleString()} hrs`;
    if (metricRiskReduced) metricRiskReduced.textContent = `${(99.0 + Math.min(0.9, revisions * 0.01)).toFixed(1)}%`;
  }

  [inputTeam, inputHours, inputRate, inputRevisions].forEach(input => {
    if (input) input.addEventListener('input', calculateROI);
  });
  calculateROI();

  /* --------------------------------------------------------------------------
     5. FAQ ACCORDION
     -------------------------------------------------------------------------- */
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const trigger = item.querySelector('.faq-trigger');
    if (trigger) {
      trigger.addEventListener('click', () => {
        const isActive = item.classList.contains('active');
        faqItems.forEach(i => i.classList.remove('active'));
        if (!isActive) item.classList.add('active');
      });
    }
  });

  /* --------------------------------------------------------------------------
     6. PRESENTATION MODE PITCH DECK VIEWER (FOR SLIDES 1, 2, 3, 4)
     -------------------------------------------------------------------------- */
  const btnPresentationMode = document.getElementById('btnPresentationMode');
  const footerOpenPitch = document.getElementById('footerOpenPitch');
  const pitchModal = document.getElementById('pitchModal');
  const pitchBackdrop = document.getElementById('pitchBackdrop');
  const btnClosePitchModal = document.getElementById('btnClosePitchModal');
  const deckViewport = document.getElementById('deckViewport');
  const deckSlideTitle = document.getElementById('deckSlideTitle');
  const btnDeckPrev = document.getElementById('btnDeckPrev');
  const btnDeckNext = document.getElementById('btnDeckNext');
  const deckIndicators = document.querySelectorAll('.deck-slide-indicators .indicator');

  let currentSlide = 1;
  const slideData = [
    {
      title: 'Slide 1: Existing Problem vs Proposed Solution',
      html: `
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; height: 100%;">
          <div style="background: #FEF2F2; border: 1px solid #FECACA; border-radius: 8px; padding: 20px;">
            <h3 style="color: #DC2626; font-size: 1.15rem; margin-bottom: 12px; font-weight: 800;">EXISTING PROBLEM</h3>
            <ul style="line-height: 1.8; font-size: 0.95rem; color: #7F1D1D; padding-left: 18px;">
              <li>Many documents are stored in different places.</li>
              <li>The same document may have many versions.</li>
              <li>Old information can be retrieved.</li>
              <li>Finding the correct document takes time.</li>
              <li>Wrong information can lead to wrong decisions.</li>
              <li>Users may not trust the AI answer.</li>
            </ul>
          </div>
          <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 20px;">
            <h3 style="color: #1E40AF; font-size: 1.15rem; margin-bottom: 12px; font-weight: 800;">PROPOSED SOLUTION</h3>
            <ul style="line-height: 1.8; font-size: 0.95rem; color: #1E3A8A; padding-left: 18px;">
              <li>Find the right document quickly.</li>
              <li>Find the latest document version.</li>
              <li>Understand the document content.</li>
              <li>Find the most useful information.</li>
              <li>Give a clear and correct answer.</li>
              <li>Show the source of the answer.</li>
              <li>Reduce wrong and outdated answers.</li>
            </ul>
          </div>
        </div>
      `
    },
    {
      title: 'Slide 2: Idea Overview',
      html: `
        <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 8px; padding: 24px;">
          <h3 style="font-family: 'Newsreader', serif; font-size: 1.4rem; color: #1E40AF; margin-bottom: 16px;">IDEA OVERVIEW</h3>
          <ul style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; list-style: none; font-size: 0.95rem;">
            <li style="background: #FFFFFF; padding: 10px 14px; border-radius: 6px; border-left: 4px solid #2563EB;">➔ A smart system for understanding documents.</li>
            <li style="background: #FFFFFF; padding: 10px 14px; border-radius: 6px; border-left: 4px solid #2563EB;">➔ Users can upload different types of documents.</li>
            <li style="background: #FFFFFF; padding: 10px 14px; border-radius: 6px; border-left: 4px solid #2563EB;">➔ The system reads and understands the content.</li>
            <li style="background: #FFFFFF; padding: 10px 14px; border-radius: 6px; border-left: 4px solid #2563EB;">➔ It finds the information related to the question.</li>
            <li style="background: #FFFFFF; padding: 10px 14px; border-radius: 6px; border-left: 4px solid #2563EB;">➔ It checks the correct document version.</li>
            <li style="background: #FFFFFF; padding: 10px 14px; border-radius: 6px; border-left: 4px solid #2563EB;">➔ It gives answers based on the documents.</li>
            <li style="background: #FFFFFF; padding: 10px 14px; border-radius: 6px; border-left: 4px solid #2563EB;">➔ It shows the source and supporting information.</li>
            <li style="background: #FFFFFF; padding: 10px 14px; border-radius: 6px; border-left: 4px solid #2563EB;">➔ It helps users make faster decisions.</li>
          </ul>
        </div>
      `
    },
    {
      title: 'Slide 3: System Workflow (6 Stages)',
      html: `
        <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; text-align: center;">
          <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 12px 6px;">
            <div style="background: #2563EB; color: #FFF; width: 26px; height: 26px; border-radius: 50%; margin: 0 auto 8px auto; line-height: 26px; font-weight: bold;">1</div>
            <strong style="font-size: 0.8rem; display: block; margin-bottom: 4px;">Input Documents</strong>
            <span style="font-size: 0.68rem; color: #64748B;">PDF, DOCX, PPT, TXT</span>
          </div>
          <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 12px 6px;">
            <div style="background: #2563EB; color: #FFF; width: 26px; height: 26px; border-radius: 50%; margin: 0 auto 8px auto; line-height: 26px; font-weight: bold;">2</div>
            <strong style="font-size: 0.8rem; display: block; margin-bottom: 4px;">Read & Understand</strong>
            <span style="font-size: 0.68rem; color: #64748B;">Extract text & semantics</span>
          </div>
          <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 12px 6px;">
            <div style="background: #2563EB; color: #FFF; width: 26px; height: 26px; border-radius: 50%; margin: 0 auto 8px auto; line-height: 26px; font-weight: bold;">3</div>
            <strong style="font-size: 0.8rem; display: block; margin-bottom: 4px;">Store with Version</strong>
            <span style="font-size: 0.68rem; color: #15803D; font-weight: bold;">v1.0, v2.0, v3.0 ✔</span>
          </div>
          <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 12px 6px;">
            <div style="background: #2563EB; color: #FFF; width: 26px; height: 26px; border-radius: 50%; margin: 0 auto 8px auto; line-height: 26px; font-weight: bold;">4</div>
            <strong style="font-size: 0.8rem; display: block; margin-bottom: 4px;">User Question</strong>
            <span style="font-size: 0.68rem; color: #64748B;">Natural language query</span>
          </div>
          <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 12px 6px;">
            <div style="background: #2563EB; color: #FFF; width: 26px; height: 26px; border-radius: 50%; margin: 0 auto 8px auto; line-height: 26px; font-weight: bold;">5</div>
            <strong style="font-size: 0.8rem; display: block; margin-bottom: 4px;">Find Latest Version</strong>
            <span style="font-size: 0.68rem; color: #15803D;">Retrieve valid v3.0</span>
          </div>
          <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 12px 6px;">
            <div style="background: #2563EB; color: #FFF; width: 26px; height: 26px; border-radius: 50%; margin: 0 auto 8px auto; line-height: 26px; font-weight: bold;">6</div>
            <strong style="font-size: 0.8rem; display: block; margin-bottom: 4px;">Structured Output</strong>
            <span style="font-size: 0.68rem; color: #1E40AF; font-weight: bold;">Source, Version, Page, Evidence</span>
          </div>
        </div>
      `
    },
    {
      title: 'Slide 4: Target Users + Use Cases',
      html: `
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
          <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 16px; border-radius: 8px;">
            <h4 style="color: #1E40AF; margin-bottom: 10px; font-size: 1.05rem;">TARGET USERS</h4>
            <ul style="line-height: 2; font-size: 0.95rem; color: #0F172A; list-style-type: square; padding-left: 20px;">
              <li>Company employees</li>
              <li>Engineers</li>
              <li>Government officers</li>
              <li>Finance and compliance teams</li>
              <li>Healthcare staff</li>
            </ul>
          </div>
          <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 16px; border-radius: 8px;">
            <h4 style="color: #059669; margin-bottom: 10px; font-size: 1.05rem;">USE CASES</h4>
            <ul style="line-height: 2; font-size: 0.95rem; color: #0F172A; list-style-type: circle; padding-left: 20px;">
              <li>Company policies and rules</li>
              <li>Machine manuals and instructions</li>
              <li>Government rules and circulars</li>
              <li>Finance and compliance documents</li>
              <li>Healthcare guidelines and SOPs</li>
            </ul>
          </div>
        </div>
      `
    }
  ];

  function showSlide(index) {
    currentSlide = index;
    const slide = slideData[index - 1];
    if (!slide) return;

    if (deckSlideTitle) deckSlideTitle.textContent = slide.title;
    if (deckViewport) deckViewport.innerHTML = slide.html;

    deckIndicators.forEach(ind => {
      ind.classList.toggle('active', parseInt(ind.dataset.slide, 10) === currentSlide);
    });

    if (btnDeckPrev) btnDeckPrev.disabled = currentSlide === 1;
    if (btnDeckNext) btnDeckNext.disabled = currentSlide === slideData.length;
  }

  function openModal() {
    if (pitchModal) {
      pitchModal.style.display = 'flex';
      showSlide(1);
    }
  }

  function closeModal() {
    if (pitchModal) pitchModal.style.display = 'none';
  }

  if (btnPresentationMode) btnPresentationMode.addEventListener('click', openModal);
  if (footerOpenPitch) footerOpenPitch.addEventListener('click', openModal);
  if (btnClosePitchModal) btnClosePitchModal.addEventListener('click', closeModal);
  if (pitchBackdrop) pitchBackdrop.addEventListener('click', closeModal);

  if (btnDeckPrev) {
    btnDeckPrev.addEventListener('click', () => {
      if (currentSlide > 1) showSlide(currentSlide - 1);
    });
  }

  if (btnDeckNext) {
    btnDeckNext.addEventListener('click', () => {
      if (currentSlide < slideData.length) showSlide(currentSlide + 1);
    });
  }

  deckIndicators.forEach(ind => {
    ind.addEventListener('click', () => {
      showSlide(parseInt(ind.dataset.slide, 10));
    });
  });

});
