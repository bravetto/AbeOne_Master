'use strict';

const BIAS_GUARD_VARS = {
  INJECTED: 'biasGuardInjected',
  DISABLED: 'biasGuardDisabled',
  OBSERVER: 'biasGuardObserver',
  CLERK_DETECTED: 'biasGuardClerkDetected',
  RESCAN_TIMEOUT: 'biasguardRescanTimeout',
  CLEANUP: 'biasGuardCleanup'
};

const ORIGINAL_METHODS = {
  CREATE_ELEMENT: 'originalCreateElement',
  QUERY_SELECTOR: 'originalQuerySelector',
  QUERY_SELECTOR_ALL: 'originalQuerySelectorAll',
  MUTATION_OBSERVER: 'originalMutationObserver'
};

/**
 * Set BiasGuard window variables
 */
function setBiasGuardState(injected = true, disabled = false) {
  return () => {
    window[BIAS_GUARD_VARS.INJECTED] = injected;
    window[BIAS_GUARD_VARS.DISABLED] = disabled;

    if (injected && !disabled) {
      if (window[ORIGINAL_METHODS.CREATE_ELEMENT]) {
        document.createElement = window[ORIGINAL_METHODS.CREATE_ELEMENT];
        document.querySelector = window[ORIGINAL_METHODS.QUERY_SELECTOR];
        document.querySelectorAll = window[ORIGINAL_METHODS.QUERY_SELECTOR_ALL];
      }
      if (window[ORIGINAL_METHODS.MUTATION_OBSERVER]) {
        window.MutationObserver = window[ORIGINAL_METHODS.MUTATION_OBSERVER];
      }
    }
  };
}

/**
 * Check if Clerk is detected on the page
 */
function checkClerkDetection() {
  return () => {
    if (window.Clerk || document.querySelector('[data-clerk]') || document.querySelector('[class*="clerk"]')) {
      console.log('Clerk detected on page, BiasGuard will not interfere with authentication');
      window[BIAS_GUARD_VARS.CLERK_DETECTED] = true;
      return true;
    }
    return false;
  };
}

/**
 * Comprehensive BiasGuard cleanup function
 */
function cleanupBiasGuard() {
  return () => {
    window[BIAS_GUARD_VARS.DISABLED] = true;
    window[BIAS_GUARD_VARS.INJECTED] = false;

    if (window[BIAS_GUARD_VARS.OBSERVER]) {
      console.log('Disconnecting BiasGuard observer');
      window[BIAS_GUARD_VARS.OBSERVER].disconnect();
      window[BIAS_GUARD_VARS.OBSERVER] = null;
    }

    window.addToChat = function() {
      return;
    };

    if (window[ORIGINAL_METHODS.CREATE_ELEMENT]) {
      document.createElement = window[ORIGINAL_METHODS.CREATE_ELEMENT];
      document.querySelector = window[ORIGINAL_METHODS.QUERY_SELECTOR];
      document.querySelectorAll = window[ORIGINAL_METHODS.QUERY_SELECTOR_ALL];
    }

    if (window[ORIGINAL_METHODS.MUTATION_OBSERVER]) {
      window.MutationObserver = window[ORIGINAL_METHODS.MUTATION_OBSERVER];
    }

    removeBiasGuardElements();
    clearBiasGuardVariables();
  };
}

/**
 * Remove all BiasGuard UI elements
 */
function removeBiasGuardElements() {
  const biasGuardBtn = document.getElementById('biasguard-chat-btn');
  if (biasGuardBtn) {
    biasGuardBtn.remove();
  }

  const buttons = document.querySelectorAll('button');
  buttons.forEach((button) => {
    if (button.innerHTML && button.innerHTML.includes('🛡️')) {
      button.remove();
    }
    if (button.title && button.title.includes('BiasGuard')) {
      button.remove();
    }
    if (
      button.id === 'biasguard-chat-btn' ||
      (button.title && button.title.includes('BiasGuard')) ||
      (button.innerHTML &&
        button.innerHTML.includes('🛡️') &&
        button.innerHTML.includes('BiasGuard'))
    ) {
      button.remove();
    }
  });

  // Remove styles
  const biasGuardStyles = document.getElementById('biasguard-styles');
  if (biasGuardStyles) {
    biasGuardStyles.remove();
  }

  // Remove BiasGuard elements
  const biasGuardElements = document.querySelectorAll(
    '[id*="biasguard"], [class*="biasguard"]'
  );
  biasGuardElements.forEach((element) => {
    if (element.id && element.id.includes('biasguard')) {
      element.remove();
    }
    if (element.className && element.className.includes('biasguard')) {
      element.remove();
    }
  });

  const notification = document.getElementById('biasguard-notification');
  if (notification) {
    notification.remove();
  }
}

/**
 * Clear all BiasGuard window variables
 */
function clearBiasGuardVariables() {
  delete window[BIAS_GUARD_VARS.OBSERVER];
  delete window[BIAS_GUARD_VARS.INJECTED];
  delete window.addToChat;
  delete window.createBiasGuardButton;
  delete window.findChatInput;
  delete window.quickBias;
  delete window.detectJWTToken;
  delete window[BIAS_GUARD_VARS.CLEANUP];
  delete window[BIAS_GUARD_VARS.RESCAN_TIMEOUT];
}

/**
 * Get injection state from storage
 */
async function getInjectionState() {
  try {
    const { injectionEnabled } = await chrome.storage.local.get(['injectionEnabled']);
    return injectionEnabled || false;
  } catch (error) {
    return false;
  }
}

/**
 * Set injection state in storage
 */
async function setInjectionState(enabled) {
  try {
    await chrome.storage.local.set({ injectionEnabled: enabled });
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * Check if BiasGuard is already injected
 */
function checkInjectionStatus() {
  return () => window[BIAS_GUARD_VARS.INJECTED];
}

/**
 * Execute script injection with error handling
 */
async function executeScriptInjection(tabId, func, files = null) {
  try {
    if (files) {
      await chrome.scripting.executeScript({
        target: { tabId },
        files: files
      });
    } else {
      await chrome.scripting.executeScript({
        target: { tabId },
        func: func
      });
    }
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * Get all tabs for injection
 */
async function getAllTabs() {
  try {
    return await chrome.tabs.query({
      url: ['http://*/*', 'https://*/*']
    });
  } catch (error) {
    return [];
  }
}

// Export utilities
window.BiasGuardUtils = {
  setBiasGuardState,
  checkClerkDetection,
  cleanupBiasGuard,
  removeBiasGuardElements,
  clearBiasGuardVariables,
  getInjectionState,
  setInjectionState,
  checkInjectionStatus,
  executeScriptInjection,
  getAllTabs,
  BIAS_GUARD_VARS,
  ORIGINAL_METHODS
};
