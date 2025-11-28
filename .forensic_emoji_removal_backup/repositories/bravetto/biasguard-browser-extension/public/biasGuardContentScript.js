// BiasGuard Content Script - Website Bias Detection
// This script runs on all websites to detect bias words and provide feedback

(function () {
  'use strict';

  // Configuration
  const CONFIG = {
    scanDelay: 1000,
    highlightDuration: 0,
    maxHighlights: 50,
    debounceDelay: 300,
    periodicCheckInterval: 0,
    minContentLength: 50,
    minWordCount: 10,
    rescanCooldown: 2000,
  };

  let isScanning = false;
  let hasScanned = false;
  let scanResults = [];
  let highlightElements = [];
  let observer = null;
  let lastContentHash = '';
  let rescanTimeout = null;
  let periodicCheckInterval = null;
  let isUpdatingDOM = false;
  let lastScanTime = 0;

  async function initializeBiasDetection() {
    try {
      const { injectionEnabled } = await chrome.storage.local.get([
        'injectionEnabled',
      ]);
      if (!injectionEnabled) {
        return;
      }

      await waitForBiasDetectionScript();
      await scanPageForBias();
      setupContentObserver();


      setTimeout(() => {
        highlightWord('test', 'test', 'low');
      }, 2000);
    } catch (error) {
      console.error('BiasGuard: Failed to initialize bias detection:', error);
    }
  }

  function waitForBiasDetectionScript() {
    return new Promise((resolve, reject) => {
      let attempts = 0;
      const maxAttempts = 30;

      const checkScript = () => {
        attempts++;

        if (typeof window.BiasDetectScript !== 'undefined') {
          resolve();
        } else if (attempts >= maxAttempts) {
          reject(new Error('Bias detection script not available'));
        } else {
          setTimeout(checkScript, 100);
        }
      };
      checkScript();
    });
  }

  async function scanPageForBias() {
    if (isScanning) return;

    const now = Date.now();
    if (now - lastScanTime < 2000) {
      return;
    }

    isScanning = true;
    lastScanTime = now;

    try {
      const textContent = extractTextContent();

      if (!textContent || textContent.length < 10) {
        return;
      }

      const results = await window.BiasDetectScript.analyzeBiasEnhanced(
        textContent
      );

      if (results.biasScore > 0.1) {
        scanResults = results;
        hasScanned = true;

        showBiasResults(results);
        highlightBiasWords(results.traditionalResults);
      } else {
        hasScanned = true;
      }
    } catch (error) {
      console.error('BiasGuard: Error during bias scan:', error);
    } finally {
      isScanning = false;
    }
  }

  function extractTextContent() {
    return extractTextContentFallback();
  }

  function extractTextContentFallback() {
    const textElements = document.querySelectorAll(
      'p, div, span, h1, h2, h3, h4, h5, h6, li, td, th, a, button, label, article, section, main, aside, header, footer, nav'
    );
    const textContent = Array.from(textElements)
      .filter((el) => isElementVisible(el))
      .map((el) => el.textContent?.trim())
      .filter((text) => text && text.length > 2)
      .join(' ');

    return textContent;
  }

  function isElementVisible(element) {
    if (!element) return false;

    const style = window.getComputedStyle(element);
    if (
      style.display === 'none' ||
      style.visibility === 'hidden' ||
      style.opacity === '0' ||
      element.hidden
    ) {
      return false;
    }

    const rect = element.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) {
      return false;
    }

    if (rect.top < -1000 || rect.left < -1000) {
      return false;
    }

    const tagName = element.tagName.toLowerCase();
    if (
      ['script', 'style', 'meta', 'link', 'noscript', 'template'].includes(
        tagName
      )
    ) {
      return false;
    }

    if (
      element.classList.contains('sr-only') ||
      element.classList.contains('visually-hidden') ||
      element.classList.contains('hidden') ||
      element.getAttribute('aria-hidden') === 'true'
    ) {
      return false;
    }

    return true;
  }

  function generateContentHash() {
    const textContent = extractTextContent();
    let hash = 0;
    for (let i = 0; i < textContent.length; i++) {
      const char = textContent.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash;
    }
    return hash.toString();
  }

  function hasContentChanged() {
    const currentHash = generateContentHash();
    if (currentHash !== lastContentHash) {
      lastContentHash = currentHash;
      return true;
    }
    return false;
  }

  function detectContentChanges() {
    const currentContent = extractTextContent();
    const currentLength = currentContent.length;
    const currentWords = currentContent.split(/\s+/).length;

    if (!window.biasGuardContentMetrics) {
      window.biasGuardContentMetrics = {
        length: currentLength,
        words: currentWords,
        hash: generateContentHash(),
        visibleElements: getVisibleElementCount(),
      };
      return false;
    }

    const prevMetrics = window.biasGuardContentMetrics;
    const lengthChange = Math.abs(currentLength - prevMetrics.length);
    const wordChange = Math.abs(currentWords - prevMetrics.words);
    const hashChanged = generateContentHash() !== prevMetrics.hash;
    const visibleElementsChanged =
      Math.abs(getVisibleElementCount() - prevMetrics.visibleElements) > 0;

    window.biasGuardContentMetrics = {
      length: currentLength,
      words: currentWords,
      hash: generateContentHash(),
      visibleElements: getVisibleElementCount(),
      lastContent: currentContent,
    };

    return (
      hashChanged ||
      lengthChange > 50 ||
      wordChange > 10 ||
      visibleElementsChanged
    );
  }

  function getVisibleElementCount() {
    const elements = document.querySelectorAll(
      'p, div, span, h1, h2, h3, h4, h5, h6, li, td, th, a, button, label, article, section, main, aside, header, footer, nav'
    );
    return Array.from(elements).filter((el) => isElementVisible(el)).length;
  }

  function shouldTriggerRescan(changeType, mutation) {
    const now = Date.now();

    if (now - lastScanTime < CONFIG.rescanCooldown) {
      return false;
    }

    const currentContent = extractTextContent();
    if (currentContent.length < CONFIG.minContentLength) {
      return false;
    }

    switch (changeType) {
      case 'textContent':
        return mutation.target.textContent.trim().length > 20;

      case 'childList':
        return Array.from(mutation.addedNodes).some((node) => {
          if (node.nodeType === Node.TEXT_NODE) {
            return node.textContent.trim().length > 20;
          }
          if (node.nodeType === Node.ELEMENT_NODE) {
            return node.textContent && node.textContent.trim().length > 50;
          }
          return false;
        });

      case 'attributes':
        const contentAttributes = ['data-content', 'data-text', 'aria-label'];
        return contentAttributes.includes(mutation.attributeName);

      default:
        return true;
    }
  }

  function showBiasResults(results) {
    const banner = createBiasNotification(results);
    document.body.appendChild(banner);

    setTimeout(() => {
      if (banner.parentNode) {
        banner.parentNode.removeChild(banner);
      }
    }, 10000);
  }

  function createBiasNotification(results) {
    const banner = document.createElement('div');
    banner.id = 'biasguard-notification';
    banner.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: ${getSeverityColor(results.severity)};
      color: white;
      padding: 8px 12px;
      border-radius: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
      z-index: 10000;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      gap: 6px;
      min-width: 80px;
    `;

    const severityText =
      results.severity.charAt(0).toUpperCase() + results.severity.slice(1);
    const scorePercent = Math.round(results.biasScore * 100);

    banner.innerHTML = `
      <span style="font-size: 14px;">🛡️</span>
      <span>${severityText}</span>
      <button id="biasguard-dismiss" style="background: none; border: none; color: white; font-size: 12px; cursor: pointer; opacity: 0.7; padding: 0; margin-left: 4px;" title="Dismiss">×</button>
    `;

    banner.addEventListener('click', (e) => {
      if (e.target.id !== 'biasguard-dismiss') {
        showDetailedResults(results);
      }
    });

    const dismissButton = banner.querySelector('#biasguard-dismiss');
    if (dismissButton) {
      dismissButton.addEventListener('click', (e) => {
        e.stopPropagation();
        clearHighlights();
        banner.remove();
      });
    }

    return banner;
  }

  function getSeverityColor(severity) {
    switch (severity) {
      case 'critical':
        return '#dc3545';
      case 'high':
        return '#fd7e14';
      case 'medium':
        return '#ffc107';
      case 'low':
        return '#28a745';
      default:
        return '#6c757d';
    }
  }

  function showDetailedResults(results) {
    const existingModal = document.getElementById('biasguard-modal');
    if (existingModal) {
      existingModal.remove();
    }

    const modal = document.createElement('div');
    modal.id = 'biasguard-modal';
    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.5);
      z-index: 10001;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    `;

    const modalContent = document.createElement('div');
    modalContent.style.cssText = `
      background: white;
      border-radius: 12px;
      padding: 24px;
      max-width: 600px;
      max-height: 80vh;
      overflow-y: auto;
      box-shadow: 0 8px 32px rgba(0,0,0,0.3);
      border: 1px solid #e9ecef;
    `;

    modalContent.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 2px solid #e9ecef;">
        <h2 style="margin: 0; color: #2c3e50; font-weight: 600;">🛡️ BiasGuard Analysis</h2>
        <div style="display: flex; gap: 10px; align-items: center;">
          <button id="biasguard-clear-highlights" style="background: #dc3545; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: 500; box-shadow: 0 2px 4px rgba(220,53,69,0.2);">Clear Highlights</button>
          <button id="biasguard-close" style="background: #6c757d; color: white; border: none; font-size: 18px; cursor: pointer; padding: 6px 10px; border-radius: 6px; font-weight: bold;">×</button>
        </div>
      </div>

      <div style="margin-bottom: 20px;">
        <div style="display: flex; gap: 16px; margin-bottom: 16px;">
          <div style="flex: 1; text-align: center; padding: 12px; background: #f8f9fa; border-radius: 8px;">
            <div style="font-size: 24px; font-weight: bold; color: ${getSeverityColor(
              results.severity
            )};">
              ${Math.round(results.biasScore * 100)}%
            </div>
            <div style="font-size: 12px; color: #666;">Bias Score</div>
          </div>
          <div style="flex: 1; text-align: center; padding: 12px; background: #f8f9fa; border-radius: 8px;">
            <div style="font-size: 18px; font-weight: bold; color: ${getSeverityColor(
              results.severity
            )};">
              ${results.severity.toUpperCase()}
            </div>
            <div style="font-size: 12px; color: #666;">Severity</div>
          </div>
        </div>
      </div>

      <div style="margin-bottom: 20px;">
        <h3 style="margin: 0 0 12px 0; color: #333;">Detected Terms (${
          results.detectedWords.length
        })</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
          ${results.detectedWords
            .map(
              (word) => `
            <span style="background: #007bff; color: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 500; box-shadow: 0 2px 4px rgba(0,123,255,0.2);">
              ${word}
            </span>
          `
            )
            .join('')}
        </div>
      </div>

      <div style="margin-bottom: 20px;">
        <h3 style="margin: 0 0 12px 0; color: #333;">Categories</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
          ${results.categories
            .map(
              (category) => `
            <span style="background: #28a745; color: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 500; box-shadow: 0 2px 4px rgba(40,167,69,0.2);">
              ${category.replace(/_/g, ' ')}
            </span>
          `
            )
            .join('')}
        </div>
      </div>

      ${
        results.priorityActions.length > 0
          ? `
        <div style="margin-bottom: 20px;">
          <h3 style="margin: 0 0 12px 0; color: #333;">Priority Actions</h3>
          <ul style="margin: 0; padding-left: 20px;">
            ${results.priorityActions
              .map(
                (action) =>
                  `<li style="margin-bottom: 8px; color: #555;">${action}</li>`
              )
              .join('')}
          </ul>
        </div>
      `
          : ''
      }

      ${
        results.recommendations.length > 0
          ? `
        <div>
          <h3 style="margin: 0 0 12px 0; color: #333;">Recommendations</h3>
          <ul style="margin: 0; padding-left: 20px;">
            ${results.recommendations
              .map(
                (rec) =>
                  `<li style="margin-bottom: 8px; color: #555;">${rec}</li>`
              )
              .join('')}
          </ul>
        </div>
      `
          : ''
      }
    `;

    modal.appendChild(modalContent);
    document.body.appendChild(modal);

    document.getElementById('biasguard-close').addEventListener('click', () => {
      modal.remove();
    });

    document
      .getElementById('biasguard-clear-highlights')
      .addEventListener('click', () => {
        clearHighlights();
        const notification = document.getElementById('biasguard-notification');
        if (notification) {
          notification.remove();
        }
      });

    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.remove();
      }
    });
  }

  function highlightBiasWords(results) {
    isUpdatingDOM = true;

    clearHighlights();

    let highlightCount = 0;
    const maxHighlights = CONFIG.maxHighlights;

    results.forEach((result) => {
      if (highlightCount >= maxHighlights) return;

      const words = result.matched.split(' ');

      words.forEach((word) => {
        if (highlightCount >= maxHighlights) return;

        const cleanWord = word.replace(/[^\w]/g, '');
        if (cleanWord.length < 2) return;

        highlightWord(cleanWord, result.category, result.severity);
        highlightCount++;
      });
    });

    setTimeout(() => {
      isUpdatingDOM = false;
    }, 100);

    if (CONFIG.highlightDuration > 0) {
      setTimeout(() => {
        clearHighlights();
      }, CONFIG.highlightDuration);
    }
  }

  function rehighlightExistingResults() {
    if (
      scanResults &&
      scanResults.traditionalResults &&
      scanResults.traditionalResults.length > 0
    ) {
      highlightBiasWords(scanResults.traditionalResults);
    }
  }

  function showHighlightTooltip(event, highlightElement) {
    const existingTooltip = document.getElementById('biasguard-tooltip');
    if (existingTooltip) {
      existingTooltip.remove();
    }

    const category = highlightElement.getAttribute('data-category');
    const severity = highlightElement.getAttribute('data-severity');
    const word = highlightElement.getAttribute('data-word');

    let resultData = null;
    if (scanResults && scanResults.traditionalResults) {
      resultData = scanResults.traditionalResults.find((result) =>
        result.matched.toLowerCase().includes(word.toLowerCase())
      );
    }

    const tooltip = document.createElement('div');
    tooltip.id = 'biasguard-tooltip';
    tooltip.style.cssText = `
      position: absolute;
      background: #2c3e50;
      color: white;
      padding: 12px 16px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      z-index: 10002;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 13px;
      max-width: 300px;
      line-height: 1.4;
      pointer-events: none;
    `;

    const severityColor = getSeverityColor(severity);
    let score = 50; // Default score

    if (resultData && resultData.score !== undefined) {
      if (resultData.score > 1) {
        score = Math.round(resultData.score);
      } else {
        score = Math.round(resultData.score * 100);
      }

      score = Math.max(1, Math.min(100, score));
    }

    tooltip.innerHTML = `
      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
        <div style="width: 8px; height: 8px; border-radius: 50%; background: ${severityColor};"></div>
        <strong style="color: ${severityColor};">${severity.toUpperCase()}</strong>
        <span style="color: #bdc3c7;">•</span>
        <span style="color: #ecf0f1;">${category.replace(/_/g, ' ')}</span>
      </div>
      <div style="margin-bottom: 8px;">
        <strong>Word:</strong> "${word}" <br>
        <!-- <strong>Score:</strong> ${score}% -->
      </div>
      ${
        resultData &&
        resultData.suggestions &&
        resultData.suggestions.length > 0
          ? `
        <div>
          <strong style="color: #3498db;">Suggestions:</strong><br>
          ${resultData.suggestions
            .slice(0, 3)
            .map((suggestion) => `• ${suggestion}`)
            .join('<br>')}
        </div>
      `
          : `
        <div style="color: #95a5a6; font-style: italic;">
          No specific suggestions available
        </div>
      `
      }
    `;

    document.body.appendChild(tooltip);

    const rect = highlightElement.getBoundingClientRect();
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollLeft =
      window.pageXOffset || document.documentElement.scrollLeft;

    tooltip.style.position = 'absolute';
    tooltip.style.left = '0px';
    tooltip.style.top = '0px';
    tooltip.style.visibility = 'hidden';
    tooltip.style.display = 'block';

    const tooltipRect = tooltip.getBoundingClientRect();

    let left = rect.left + scrollLeft + rect.width / 2 - tooltipRect.width / 2;
    let top = rect.top + scrollTop - tooltipRect.height - 10;

    if (left < scrollLeft + 10) {
      left = scrollLeft + 10;
    } else if (left + tooltipRect.width > scrollLeft + window.innerWidth - 10) {
      left = scrollLeft + window.innerWidth - tooltipRect.width - 10;
    }

    if (top < scrollTop + 10) {
      top = rect.bottom + scrollTop + 10;
    }

    tooltip.style.left = `${left}px`;
    tooltip.style.top = `${top}px`;
    tooltip.style.visibility = 'visible';

    setTimeout(() => {
      if (tooltip.parentNode) {
        tooltip.remove();
      }
    }, 5000);

    const removeTooltip = (e) => {
      if (!tooltip.contains(e.target) && !highlightElement.contains(e.target)) {
        tooltip.remove();
        document.removeEventListener('click', removeTooltip);
      }
    };

    setTimeout(() => {
      document.addEventListener('click', removeTooltip);
    }, 100);
  }

  function shouldPerformFullRescan() {
    if (
      !scanResults ||
      !scanResults.traditionalResults ||
      scanResults.traditionalResults.length === 0
    ) {
      return true;
    }

    if (hasContentChanged()) {
      return true;
    }

    const currentContent = extractTextContent();
    const previousContent = window.biasGuardContentMetrics?.lastContent || '';

    if (currentContent.length > previousContent.length + 100) {
      return true;
    }

    return false;
  }

  function highlightWord(word, category, severity) {

    const cleanWord = word.replace(/[^\w]/g, '');

    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
      null,
      false
    );

    const textNodes = [];
    let node;
    while ((node = walker.nextNode())) {
      if (node.textContent.toLowerCase().includes(word.toLowerCase())) {
        textNodes.push(node);
      }
    }

    textNodes.forEach((textNode, index) => {
      const parent = textNode.parentNode;
      if (parent && !parent.closest('.biasguard-highlight')) {
        const regex = new RegExp(
          `\\b${word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`,
          'gi'
        );
        const highlightedHTML = textNode.textContent.replace(regex, (match) => {
          return `<span class="biasguard-highlight biasguard-${severity}" data-category="${category}" data-severity="${severity}" data-word="${cleanWord}" title="Click for details">${match}</span>`;
        });

        if (highlightedHTML !== textNode.textContent) {
          try {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = highlightedHTML;

            const fragment = document.createDocumentFragment();
            while (tempDiv.firstChild) {
              fragment.appendChild(tempDiv.firstChild);
            }

            parent.replaceChild(fragment, textNode);

            const newHighlights = parent.querySelectorAll(
              '.biasguard-highlight'
            );
            newHighlights.forEach((highlight) => {
              if (!highlight.hasAttribute('data-tooltip-added')) {
                highlight.addEventListener('click', (e) => {
                  e.stopPropagation();
                  showHighlightTooltip(e, highlight);
                });
                highlight.setAttribute('data-tooltip-added', 'true');
              }
            });
          } catch (error) {
            console.warn('BiasGuard: Failed to highlight word:', word, error);
          }
        }
      }
    });
  }

  function clearHighlights() {
    const highlights = document.querySelectorAll('.biasguard-highlight');
    highlights.forEach((highlight) => {
      const parent = highlight.parentNode;
      if (parent) {
        parent.replaceChild(
          document.createTextNode(highlight.textContent),
          highlight
        );
        parent.normalize();
      }
    });
    highlightElements = [];
  }

  function setupContentObserver() {
    if (observer) {
      observer.disconnect();
    }

    observer = new MutationObserver((mutations) => {
      if (isUpdatingDOM || isScanning) {
        return;
      }

      let hasSignificantTextChange = false;
      let hasAttributeChange = false;
      let hasTextContentChange = false;

      mutations.forEach((mutation) => {
        if (
          mutation.target.classList &&
          mutation.target.classList.contains('biasguard-highlight')
        ) {
          return;
        }

        if (
          mutation.target.id &&
          (mutation.target.id.includes('biasguard-') ||
            mutation.target.closest('[id*="biasguard-"]'))
        ) {
          return;
        }

        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
          const hasNewTextContent = Array.from(mutation.addedNodes).some(
            (node) => {
              if (
                node.nodeType === Node.ELEMENT_NODE &&
                (node.classList.contains('biasguard-highlight') ||
                  (node.id && node.id.includes('biasguard-')))
              ) {
                return false;
              }

              if (
                node.nodeType === Node.ELEMENT_NODE &&
                !isElementVisible(node)
              ) {
                return false;
              }

              const hasTextContent =
                node.nodeType === Node.TEXT_NODE ||
                (node.nodeType === Node.ELEMENT_NODE &&
                  node.textContent &&
                  node.textContent.trim().length > 20 &&
                  !node.closest('[id*="biasguard-"]'));

              return hasTextContent;
            }
          );

          if (hasNewTextContent && shouldTriggerRescan('childList', mutation)) {
            hasSignificantTextChange = true;
          }
        }

        if (
          mutation.type === 'characterData' &&
          mutation.target.textContent.trim().length > 10
        ) {
          if (shouldTriggerRescan('textContent', mutation)) {
            hasTextContentChange = true;
          }
        }

        if (mutation.type === 'attributes') {
          const importantAttributes = [
            'data-content',
            'data-text',
            'aria-label',
            'title',
          ];
          if (
            importantAttributes.includes(mutation.attributeName) &&
            shouldTriggerRescan('attributes', mutation)
          ) {
            hasAttributeChange = true;
          }
        }
      });

      if (
        hasSignificantTextChange ||
        hasTextContentChange ||
        hasAttributeChange
      ) {
        if (rescanTimeout) {
          clearTimeout(rescanTimeout);
        }

        rescanTimeout = setTimeout(() => {
          if (!isScanning && (hasContentChanged() || detectContentChanges())) {

            if (shouldPerformFullRescan()) {
              clearHighlights();
              hasScanned = false;
              scanPageForBias();
            } else {
              rehighlightExistingResults();
            }
          }
        }, CONFIG.debounceDelay);
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true,
      attributes: true,
      attributeFilter: ['data-content', 'data-text', 'aria-label', 'title'],
    });
  }

  function addHighlightStyles() {
    if (document.getElementById('biasguard-styles')) {
      return;
    }

    const style = document.createElement('style');
    style.id = 'biasguard-styles';
    style.textContent = `
      .biasguard-highlight {
        background: linear-gradient(120deg, #ffe0e0 0%, #ffe8e8 100%) !important;
        color: #d32f2f !important;
        padding: 1px 3px !important;
        border-radius: 3px !important;
        font-weight: bold !important;
        cursor: help !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        display: inline !important;
        position: relative !important;
      }

      .biasguard-highlight:hover {
        background: linear-gradient(120deg, #ffd0d0 0%, #ffe0e0 100%) !important;
        transform: scale(1.05) !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
      }

      .biasguard-critical {
        background: linear-gradient(120deg, #ffebee 0%, #fce4ec 100%) !important;
        color: #c62828 !important;
      }

      .biasguard-high {
        background: linear-gradient(120deg, #fff3e0 0%, #ffe0b2 100%) !important;
        color: #ef6c00 !important;
      }

      .biasguard-medium {
        background: linear-gradient(120deg, #fffde7 0%, #fff9c4 100%) !important;
        color: #f57f17 !important;
      }

      .biasguard-low {
        background: linear-gradient(120deg, #e8f5e8 0%, #c8e6c9 100%) !important;
        color: #2e7d32 !important;
      }

      #biasguard-notification {
        animation: slideUp 0.3s ease-out;
      }

      @keyframes slideUp {
        from {
          transform: translateY(100%);
          opacity: 0;
        }
        to {
          transform: translateY(0);
          opacity: 1;
        }
      }
    `;

    document.head.appendChild(style);
  }

  function initialize() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initialize);
      return;
    }

    addHighlightStyles();
    setTimeout(initializeBiasDetection, CONFIG.scanDelay);
  }

  function cleanup() {
    if (observer) {
      observer.disconnect();
      observer = null;
    }
    clearHighlights();

    isScanning = false;
    hasScanned = false;
    scanResults = [];

    if (window.biasGuardRescanTimeout) {
      clearTimeout(window.biasGuardRescanTimeout);
    }
    if (rescanTimeout) {
      clearTimeout(rescanTimeout);
      rescanTimeout = null;
    }
    if (periodicCheckInterval) {
      clearInterval(periodicCheckInterval);
      periodicCheckInterval = null;
    }

    const notification = document.getElementById('biasguard-notification');
    if (notification) notification.remove();

    const modal = document.getElementById('biasguard-modal');
    if (modal) modal.remove();

    const styles = document.getElementById('biasguard-styles');
    if (styles) styles.remove();
  }

  chrome.storage.onChanged.addListener((changes, namespace) => {
    if (namespace === 'local' && changes.injectionEnabled) {
      if (!changes.injectionEnabled.newValue) {
        cleanup();
      } else {
        initialize();
      }
    }
  });

  window.BiasGuardUtils = {
    cleanupBiasGuard: cleanup,
    rescanPage: scanPageForBias,
  };

  initialize();
})();
