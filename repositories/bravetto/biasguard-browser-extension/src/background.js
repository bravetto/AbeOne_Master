'use strict';

import { CONFIG } from './config.js';

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'CHECK_STORAGE') {
    chrome.storage.local.get(null, (result) => {
      sendResponse({ status: 'ok', storage: result });
    });
    return true;
  }

  if (request.type === 'CLEAR_CLERK_TOKEN') {
    const keysToRemove = [
      'clerkToken',
      'userData',
      'lastUserDataUpdate',
      'injectionEnabled',
      'biasGuardSettings',
      'biasGuardHistory',
      'biasGuardPreferences',
      'userPreferences',
      'sessionData',
      'authData',
      'userSettings'
    ];

    chrome.storage.local.remove(keysToRemove, () => {
      chrome.storage.local.clear(() => {
        chrome.storage.sync.clear(() => {
          sendResponse({ status: 'ok' });
        });
      });
    });
    return true;
  }

  if (request.type === 'AUTHENTICATED_API_CALL') {
    makeAuthenticatedRequest(request.url, request.options || {})
      .then(async (response) => {
        const responseData = await response.text();
        sendResponse({
          status: 'ok',
          statusCode: response.status,
          headers: Object.fromEntries(response.headers.entries()),
          data: responseData,
        });
      })
      .catch((error) => {
        sendResponse({ status: 'error', error: error.message });
      });
    return true;
  }

  if (request.type === 'CHECK_AUTH_STATUS') {
    checkAuthenticationStatus()
      .then(result => {
        sendResponse({ status: 'ok', authResult: result });
      })
      .catch(error => {
        sendResponse({ status: 'error', error: error.message });
      });
    return true;
  }
});

chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (
    changeInfo.status === 'complete' &&
    tab.url &&
    tab.url.startsWith('http')
  ) {
    try {
      const { injectionEnabled } = await chrome.storage.local.get(['injectionEnabled']);

      if (injectionEnabled) {
        if (!CONFIG.AUTHENTICATION_ENABLED) {
          const results = await chrome.scripting.executeScript({
            target: { tabId },
            func: () => window.biasGuardInjected,
          });

          if (!results[0]?.result) {
            await chrome.scripting.executeScript({
              target: { tabId },
              files: ["bias-words.js", "bias-suggestions.js", "bias-detect-script.js", "biasGuardContentScript.js"]
            });
          }
        } else {
          const authResult = await checkAuthenticationStatus();
          
          if (authResult.isValid) {
            const results = await chrome.scripting.executeScript({
              target: { tabId },
              func: () => window.biasGuardInjected,
            });

            if (!results[0]?.result) {
              await chrome.scripting.executeScript({
                target: { tabId },
                files: ["bias-words.js", "bias-suggestions.js", "bias-detect-script.js", "biasGuardContentScript.js"]
              });
            }
          } else if (authResult.needsCleanup) {
            await cleanupUserSession();
          }
        }
      }
    } catch (error) {
      console.error(error);
    }
  }
});

chrome.runtime.onStartup.addListener(async () => {
  const { injectionEnabled } = await chrome.storage.local.get([
    'injectionEnabled',
  ]);
  if (injectionEnabled) {
    await injectIntoExistingTabs();
  }
});

chrome.runtime.onInstalled.addListener(async () => {
  const { injectionEnabled } = await chrome.storage.local.get([
    'injectionEnabled',
  ]);
  if (injectionEnabled === undefined) {
    await chrome.storage.local.set({ injectionEnabled: false });
  } else if (injectionEnabled) {
    await injectIntoExistingTabs();
  }
});

async function injectIntoExistingTabs() {
  try {
    const tabs = await chrome.tabs.query({
      url: ['http://*/*', 'https://*/*']
    });
    const { injectionEnabled } = await chrome.storage.local.get(['injectionEnabled']);

    for (const tab of tabs) {
      try {
        if (injectionEnabled) {
          const results = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => window.biasGuardInjected,
          });

          if (!results[0]?.result) {
            await chrome.scripting.executeScript({
              target: { tabId: tab.id },
              func: () => {
                window.biasGuardInjected = true;
                window.biasGuardDisabled = false;
              },
            });
          }
        }
      } catch (error) {
        console.error(error);
      }
    }
  } catch (error) {
    console.error(error);
  }
}

async function cleanupBiasGuardInjection(tabId) {
  try {
    await chrome.scripting.executeScript({
      target: { tabId },
      func: window.BiasGuardUtils?.cleanupBiasGuard() || (() => {
        console.log('BiasGuardUtils not available, using fallback cleanup');
        window.biasGuardDisabled = true;
        window.biasGuardInjected = false;
      }),
    });
  } catch (error) {
    console.error('Cleanup failed:', error);
  }
}

async function makeAuthenticatedRequest(url, options = {}) {
  try {
    const { clerkToken } = await chrome.storage.local.get(['clerkToken']);

    if (!clerkToken) {
      throw new Error('No Clerk token available');
    }

    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${clerkToken}`,
      },
      mode: 'cors',
      credentials: 'include',
      redirect: 'manual',
    });

    if (
      response.redirected ||
      response.status === 302 ||
      response.status === 301
    ) {
      throw new Error('Authentication required - token may be expired');
    }

    return response;
  } catch (error) {
    console.error(error);
  }
}

chrome.storage.onChanged.addListener(async (changes, namespace) => {
  if (namespace === 'local' && changes.injectionEnabled) {
    const newValue = changes.injectionEnabled.newValue;

    if (!newValue) {
      try {
        const tabs = await chrome.tabs.query({
          url: ['http://*/*', 'https://*/*'],
        });

        for (const tab of tabs) {
          await cleanupBiasGuardInjection(tab.id);
        }
      } catch (error) {
        console.error(error);
      }
    }
  }
});

/**
 * Centralized authentication check function
 * Returns: { isValid: boolean, needsCleanup: boolean }
 */
async function checkAuthenticationStatus() {
  try {
    const { clerkToken } = await chrome.storage.local.get(['clerkToken']);

    if (!clerkToken) {
      return { isValid: false, needsCleanup: false };
    }

    const response = await fetch('https://api.biasguards.ai/api/v1/auth/ex-me', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${clerkToken}`,
        'Content-Type': 'application/json',
      },
      redirect: 'manual'
    });

    if (response.status === 401 || response.status === 403 || response.redirected) {
      return { isValid: false, needsCleanup: true };
    } else if (response.ok) {
      return { isValid: true, needsCleanup: false };
    } else {
      return { isValid: false, needsCleanup: true };
    }
  } catch (error) {
    return { isValid: false, needsCleanup: true };
  }
}

/**
 * Clean up user data and disable injection
 */
async function cleanupUserSession() {
  await chrome.storage.local.remove([
    'clerkToken',
    'userData',
    'lastUserDataUpdate',
    'injectionEnabled'
  ]);

  await chrome.storage.local.set({ injectionEnabled: false });

  const tabs = await chrome.tabs.query({
    url: ['http://*/*', 'https://*/*'],
  });

  for (const tab of tabs) {
    await cleanupBiasGuardInjection(tab.id);
  }
}

setInterval(async () => {
  if (!CONFIG.AUTHENTICATION_ENABLED) {
    return;
  }
  
  const authResult = await checkAuthenticationStatus();

  if (!authResult.isValid && authResult.needsCleanup) {
    await cleanupUserSession();
  }
}, 5 * 60 * 1000);
