(function() {
  'use strict';

  let biasWords = {};
  let biasWordsRegex = {};
  let biasSuggestions = {};
  let isDataLoaded = false;

  function waitForBiasData() {
    return new Promise((resolve, reject) => {
      let attempts = 0;
      const maxAttempts = 50;

      const checkData = () => {
        attempts++;

        if (typeof window.BiasWords !== 'undefined' && typeof window.BiasSuggestions !== 'undefined') {
          resolve();
        } else if (attempts >= maxAttempts) {
          resolve();
        } else {
          setTimeout(checkData, 100);
        }
      };
      checkData();
    });
  }

  const SCORING_WEIGHTS = {
    individual: 1.2,
    phrase: 1.8,
    pattern: 2.5,
    contextual: 1.5,
    categoryWeights: {
      'overconfidence': 3.0,
      'urgency': 2.5,
      'perfectionism': 2.2,
      'absolutism': 2.8,
      'simplification': 1.8,
      'proof': 2.0,
      'originality': 1.5,
      'recency': 1.3,
      'sunk_cost': 2.2,
      'bandwagon': 1.6,
      'expertise': 2.0,
      'analysis_paralysis': 1.4,
      'scope_creep': 1.7,
      'technical_debt': 1.9,
      'optimization': 1.6,
      'enhancement': 1.3,
      'gender_m': 2.5,
      'gender_f': 2.5,
      'race': 3.0,
      'age': 2.0,
      'disability': 2.8,
      'political_l': 2.2,
      'political_c': 2.2,
      'weat_career': 1.8,
      'weat_family': 1.5,
      'weat_male': 2.0,
      'weat_female': 2.0,
      'weat_european': 1.8,
      'weat_african': 1.8,
      'emotional_bias': 2.3,
      'default': 1.5
    }
  };

  const MINIMUM_SCORE_THRESHOLD = 1.0;

  async function loadBiasData() {
    if (isDataLoaded) return;

    try {
      await waitForBiasData();
      biasWords = window.BiasWords || {};
      biasWordsRegex = window.BiasWordsRegex || {};
      biasSuggestions = window.BiasSuggestions || {};
      isDataLoaded = true;
    } catch (error) {
      console.error('BiasGuard: Failed to load bias data:', error);
    }
  }

  // Get category from suggestion ID
  function getCategoryFromSuggestionId(suggestionId) {
    if (suggestionId.startsWith('s')) return 'overconfidence';
    if (suggestionId.includes('gender_')) return suggestionId;
    if (suggestionId.includes('race')) return 'race';
    if (suggestionId.includes('age')) return 'age';
    if (suggestionId.includes('disability')) return 'disability';
    if (suggestionId.includes('political_')) return suggestionId;
    if (suggestionId.includes('weat_')) return suggestionId;
    if (suggestionId.includes('emotional_bias')) return 'emotional_bias';
    return 'general';
  }

  async function detectBiasWordsInContent(text) {
    await loadBiasData();

    const results = [];
    const foundMatches = new Set();
    const lowerText = text.toLowerCase();

    const words = lowerText.match(/\b\w+(?:'\w+)?\b/g) || [];

    for (const word of words) {
      if (word.length < 2 || foundMatches.has(word)) continue;

      const wordInfo = biasWords[word];
      if (wordInfo) {
        foundMatches.add(word);
        results.push({
          word: word,
          suggestion: biasSuggestions[wordInfo] || `Bias detected: ${word}`,
          category: getCategoryFromSuggestionId(wordInfo),
          type: 'individual'
        });
      }
    }

    for (const [pattern, category] of Object.entries(biasWordsRegex)) {
      try {
        const regex = new RegExp(`\\b${pattern}\\b`, 'gi');
        const matches = lowerText.match(regex);

        if (matches) {
          matches.forEach(match => {
            if (!foundMatches.has(match)) {
              foundMatches.add(match);
              results.push({
                word: match,
                suggestion: `Bias pattern detected: ${match}`,
                category: getCategoryFromSuggestionId(category),
                type: 'pattern'
              });
            }
          });
        }
      } catch (error) {
        console.warn(`BiasGuard: Invalid regex pattern: ${pattern}`, error);
      }
    }

    return results;
  }

  async function checkBias(text, options = {}) {
    await loadBiasData();

    const results = [];
    const foundMatches = new Set();
    const wordCounts = new Map();
    const lowerText = text.toLowerCase();

    const delimitedText = lowerText.replace(/[,;|]/g, ' ');
    const words = delimitedText.match(/\b\w+(?:'\w+)?\b/g) || [];
    const phrases = delimitedText.match(/\b\w+(?:\s+\w+){1,}\b/g) || [];

    for (const word of words) {
      if (word.length >= 2) {
        wordCounts.set(word, (wordCounts.get(word) || 0) + 1);
      }
    }

    for (const word of words) {
      if (word.length < 2) continue;

      if (!foundMatches.has(word)) {
        const wordInfo = biasWords[word];
        if (wordInfo) {
          foundMatches.add(word);
          const count = wordCounts.get(word) || 1;
          const matchedText = count > 1 ? `${word} (${count} times)` : word;

          const result = {
            type: word.includes(' ') ? 'phrase' : 'individual',
            category: getCategoryFromSuggestionId(wordInfo),
            matched: matchedText,
            suggestions: [biasSuggestions[wordInfo]],
            score: 0,
            severity: 'low'
          };

          const typeWeight = SCORING_WEIGHTS[result.type] || 1.0;
          const categoryWeight = SCORING_WEIGHTS.categoryWeights[result.category] || SCORING_WEIGHTS.categoryWeights.default;
          let baseScore = (typeWeight * categoryWeight) / 2; // Scale down base scores

          if (word.toLowerCase().includes('always') || word.toLowerCase().includes('never')) {
            baseScore *= 1.3;
          }
          if (word.toLowerCase().includes('perfect') || word.toLowerCase().includes('ideal')) {
            baseScore *= 1.2;
          }
          if (word.toLowerCase().includes('urgent') || word.toLowerCase().includes('asap')) {
            baseScore *= 1.2;
          }

          result.score = Math.min(10, Math.round(baseScore * 10) / 10);
          if (result.score >= MINIMUM_SCORE_THRESHOLD) {
            if (result.score >= 7.5) result.severity = 'critical';
            else if (result.score >= 5.0) result.severity = 'high';
            else if (result.score >= 2.5) result.severity = 'medium';
            results.push(result);
          }
        }
      }
    }

    for (const [pattern, category] of Object.entries(biasWordsRegex)) {
      try {
        const regex = new RegExp(`\\b${pattern}\\b`, 'gi');
        const matches = delimitedText.match(regex);

        if (matches) {
          matches.forEach(match => {
            if (!foundMatches.has(match)) {
              foundMatches.add(match);
              const count = (delimitedText.match(new RegExp(`\\b${match.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'gi')) || []).length;
              const matchedText = count > 1 ? `${match} (${count} times)` : match;

              const result = {
                type: 'pattern',
                category: getCategoryFromSuggestionId(category),
                matched: matchedText,
                suggestions: [`Bias pattern detected: ${match}`],
                score: 0,
                severity: 'low'
              };

              const typeWeight = SCORING_WEIGHTS.pattern;
              const categoryWeight = SCORING_WEIGHTS.categoryWeights[result.category] || SCORING_WEIGHTS.categoryWeights.default;
              let baseScore = (typeWeight * categoryWeight) / 2; // Scale down base scores

              result.score = Math.min(10, Math.round(baseScore * 10) / 10);
              if (result.score >= MINIMUM_SCORE_THRESHOLD) {
                if (result.score >= 7.5) result.severity = 'critical';
                else if (result.score >= 5.0) result.severity = 'high';
                else if (result.score >= 2.5) result.severity = 'medium';
                results.push(result);
              }
            }
          });
        }
      } catch (error) {
        console.warn(`BiasGuard: Invalid regex pattern: ${pattern}`, error);
      }
    }

    return results;
  }

  async function analyzeBiasMathematically(content, previousMessages = []) {
    await loadBiasData();

    const patterns = [];
    let totalScore = 0;
    let confidence = 0.5;

    const biasResults = await detectBiasWordsInContent(content);

    if (biasResults.length > 0) {
      biasResults.forEach(result => {
        const weight = SCORING_WEIGHTS.individual;
        const categoryWeight = SCORING_WEIGHTS.categoryWeights[result.category] || 1.0;
        const finalWeight = weight * categoryWeight;

        patterns.push({
          type: result.category,
          severity: finalWeight > 2.0 ? 'high' : finalWeight > 1.5 ? 'medium' : 'low',
          matches: 1,
          intervention: result.suggestion,
          confidence: Math.min(0.9, 0.5 + (finalWeight * 0.1))
        });
        totalScore += finalWeight;
      });
    }

    confidence = Math.min(0.95, patterns.length > 0 ?
      patterns.reduce((sum, p) => sum + p.confidence, 0) / patterns.length : 0.3);

    return {
      patterns,
      totalScore: Math.min(1.0, totalScore / 20),
      confidence,
      repetitionScore: previousMessages.length > 0 ?
        calculateRepetitionScore(previousMessages) : 0
    };
  }

  async function analyzeBiasEnhanced(text, options = {}, previousMessages = []) {
    const traditionalResults = await checkBias(text, options);
    const mathematicalAnalysis = await analyzeBiasMathematically(text, previousMessages);

    const traditionalScore = traditionalResults.length > 0
      ? Math.min(1.0, traditionalResults.reduce((sum, result) => sum + result.score, 0) / 100)
      : 0;

    const mathematicalScore = Math.min(1.0, mathematicalAnalysis.totalScore);

    const unifiedScore = (traditionalScore + mathematicalScore) / 2;
    const unifiedConfidence = (mathematicalAnalysis.confidence + 0.8) / 2;

    let unifiedSeverity;
    if (unifiedScore >= 0.75) unifiedSeverity = 'critical';
    else if (unifiedScore >= 0.5) unifiedSeverity = 'high';
    else if (unifiedScore >= 0.25) unifiedSeverity = 'medium';
    else unifiedSeverity = 'low';

    const recommendations = [];
    const priorityActions = [];

    mathematicalAnalysis.patterns.forEach(pattern => {
      if (pattern.severity === 'critical' || pattern.severity === 'high') {
        priorityActions.push(pattern.intervention);
      } else {
        recommendations.push(pattern.intervention);
      }
    });

    traditionalResults.forEach(result => {
      if (result.severity === 'critical' || result.severity === 'high') {
        priorityActions.push(...result.suggestions);
      } else {
        recommendations.push(...result.suggestions);
      }
    });

    return {
      biasScore: unifiedScore,
      confidence: unifiedConfidence,
      severity: unifiedSeverity,
      traditionalResults,
      mathematicalAnalysis,
      recommendations: [...new Set(recommendations)],
      priorityActions: [...new Set(priorityActions)],
      detectedWords: traditionalResults.map(r => r.matched),
      categories: [...new Set(traditionalResults.map(r => r.category))]
    };
  }

  async function analyzeBiasRealTime(text, options = {}, previousMessages = []) {
    return await analyzeBiasEnhanced(text, options, previousMessages);
  }

  function calculateRepetitionScore(previousMessages) {
    if (previousMessages.length === 0) return 0;

    const recentMessages = previousMessages.slice(-5);
    const biasWords = ['always', 'never', 'perfect', 'ideal', 'urgent', 'asap'];

    let repetitionCount = 0;
    recentMessages.forEach(message => {
      biasWords.forEach(word => {
        if (message.toLowerCase().includes(word)) {
          repetitionCount++;
        }
      });
    });

    return Math.min(0.3, repetitionCount * 0.1);
  }

  window.BiasDetectScript = {
    loadBiasData,
    detectBiasWordsInContent,
    checkBias,
    analyzeBiasEnhanced,
    analyzeBiasRealTime,
    analyzeBiasMathematically
  };

})();
