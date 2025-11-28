'use strict';

import './popup.css';
import { CONFIG } from './config.js';

const SITE_URL = 'https://biasguards.ai';
const API_URL = 'https://api.biasguards.ai';
const CLERK_PUB_KEY = 'REPLACE_ME';
let g_User = null;
let g_InjectionEnabled = false;
let g_Clerk = null;
let g_ClerkReady = false;

const loginSection = document.getElementById('loginSection');
const dashboardSection = document.getElementById('dashboardSection');
const statusText = document
  .getElementById('statusIndicator')
  .querySelector('.status-text');
const statusDot = document
  .getElementById('statusIndicator')
  .querySelector('.status-dot');
const userName = document.getElementById('userName');
const userPlan = document.getElementById('userPlan');
const injectionToggle = document.getElementById('injectionToggle');

const initializeClerk = async () => {
  try {
    if (typeof window.Clerk === 'undefined') {
      await new Promise((resolve, reject) => {
        let attempts = 0;
        const maxAttempts = 100;

        const checkClerk = () => {
          attempts++;
          if (typeof window.Clerk !== 'undefined') {
            resolve();
          } else if (attempts >= maxAttempts) {
            reject(new Error('Clerk failed to load within timeout'));
          } else {
            setTimeout(checkClerk, 100);
          }
        };
        checkClerk();
      });
    }

    g_Clerk = window.Clerk;

    if (g_Clerk && g_Clerk.load) {
      await g_Clerk.load({
        publishableKey: CLERK_PUB_KEY,
        appearance: {
          baseTheme: undefined,
          variables: {},
          elements: {},
        },
        origin: SITE_URL,
      });
    }

    g_ClerkReady = true;

    if (g_Clerk && g_Clerk.addListener) {
      g_Clerk.addListener(({ user }) => {
        if (user) {
          g_User = {
            id: user.id,
            name:
              user.fullName ||
              user.firstName ||
              user.emailAddresses[0]?.emailAddress ||
              'User',
            email: user.emailAddresses[0]?.emailAddress || '',
            imageUrl: user.imageUrl,
          };
          showDashboardSection();
          updateUserInfo(true);

          g_Clerk.session?.getToken().then((token) => {
            if (token) {
              chrome.storage.local.set({ clerkToken: token });
            }
          });
        } else {
          g_User = null;
          showLoginSection();
          chrome.storage.local.remove(['clerkToken']);
        }
      });
    }

    if (g_Clerk && g_Clerk.user) {
      g_User = {
        id: g_Clerk.user.id,
        name:
          g_Clerk.user.fullName ||
          g_Clerk.user.firstName ||
          g_Clerk.user.emailAddresses[0]?.emailAddress ||
          'User',
        email: g_Clerk.user.emailAddresses[0]?.emailAddress || '',
        plan: 'Active',
        imageUrl: g_Clerk.user.imageUrl,
      };
      showDashboardSection();
      updateUserInfo();
    } else {
      showLoginSection();
    }
  } catch (error) {
    showLoginSection();

    const loginSection = document.getElementById('loginSection');
    if (loginSection) {
      const errorDiv = document.createElement('div');
      errorDiv.style.cssText =
        'color: #ef4444; text-align: center; margin-top: 10px; font-size: 12px;';
      errorDiv.textContent =
        'Authentication service unavailable. Please try again later.';
      loginSection.appendChild(errorDiv);

      const fallbackDiv = document.createElement('div');
      fallbackDiv.style.cssText =
        'text-align: center; margin-top: 10px; font-size: 12px;';
      fallbackDiv.innerHTML =
        '<p>Or <a href="#" id="fallbackAuth" style="color: #2563eb;">continue without authentication</a></p>';
      loginSection.appendChild(fallbackDiv);

      document.getElementById('fallbackAuth').addEventListener('click', (e) => {
        e.preventDefault();
        g_User = {
          id: 'fallback',
          name: 'Demo User',
          email: 'demo@example.com',
          plan: 'Demo',
          imageUrl: null,
        };
        showDashboardSection();
        updateUserInfo();
      });
    }
  }
};

const apiFetch = async (url, method = 'GET') => {
  try {
    let token = null;
    if (g_Clerk?.session) {
      token = await g_Clerk.session.getToken();
    } else {
      const response = await chrome.runtime.sendMessage({
        type: 'CHECK_STORAGE',
      });
      token = response?.storage?.clerkToken || null;
    }

    if (!token) {
      throw new Error('No authentication token');
    }

    const res = await fetch(`${API_URL}${url}`, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'Origin': SITE_URL,
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      redirect: 'manual',
    });

    const authStatus = res.headers.get('x-clerk-auth-status');
    if (authStatus === 'signed-out') {
      await cleanupUserSession();

      if (g_Clerk && typeof g_Clerk.signOut === 'function') {
        try {
          await g_Clerk.signOut();
        } catch (clerkError) {
          console.error('Clerk signOut error via header check:', clerkError);
        }
      }

      showLoginSection();
      throw new Error('User has been signed out');
    }

    if (res.redirected || res.status === 302 || res.status === 301) {
      throw new Error('Authentication required - token may be expired');
    }

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }

    const contentType = res.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      throw new Error(
        'Invalid response format - likely redirected to login page'
      );
    }

    const data = await res.json();
    return data;
  } catch (err) {
    throw err;
  }
};

const fetchUserInfo = async () => {
  try {
    const { clerkToken } = await chrome.storage.local.get(['clerkToken']);

    if (!clerkToken) {
      throw new Error('No authentication token available');
    }

    let userData;
    try {
      userData = await apiFetch('/api/v1/auth/ex-me');
    } catch (apiError) {
      if (apiError.message === 'User has been signed out') {
        return null;
      }
      throw apiError;
    }

    if (userData && userData.user) {
      const user = userData.user || userData;
      const subscription = userData.subscription;

      g_User = {
        id: user.id || user.userId || 'unknown',
        name:
          user.firstName && user.lastName
            ? `${user.firstName} ${user.lastName}`
            : user.firstName || user.name || user.fullName || 'User',
        email: user.email || user.emailAddress || '',
        plan: subscription?.name || 'Free',
        imageUrl:
          g_Clerk?.user?.imageUrl || user.imageUrl || user.avatar || null,
        subscription: subscription || null,
        firstName: user.firstName,
        lastName: user.lastName,
        emailVerified: user.emailVerified,
        stripeCustomerId: user.stripeCustomerId,
        teamId: user.teamId,
        teamRole: user.teamRole,
        createdAt: user.createdAt,
        updatedAt: user.updatedAt,
        subscriptionId: subscription?.id,
        subscriptionAmount: subscription?.amount,
        subscriptionCurrency: subscription?.currency,
        subscriptionInterval: subscription?.interval,
        subscriptionIntervalUnit: subscription?.intervalUnit,
        subscriptionFeatures: subscription?.features || [],
        subscriptionStartDate: subscription?.startDate,
        subscriptionEndDate: subscription?.endDate,
        subscriptionIsPaused: subscription?.isPaused,
        subscriptionIsCancelled: subscription?.isCancelled,
      };

      chrome.storage.local.set({
        userData: g_User,
        lastUserDataUpdate: Date.now()
      });

      return userData;
    }
  } catch (error) {
    if (g_Clerk && g_Clerk.user) {
      g_User = {
        id: g_Clerk.user.id,
        name: g_Clerk.user.fullName || g_Clerk.user.firstName || 'User',
        email: g_Clerk.user.emailAddresses[0]?.emailAddress || '',
        plan: 'Free',
        imageUrl: g_Clerk.user.imageUrl,
      };
    }
    throw error;
  }
};

const openSignIn = async () => {
  const loginBtn = document.getElementById('loginBtn');
  const loadingMessage = document.getElementById('loadingMessage');

  if (!g_Clerk) {
    alert('Authentication service is not available. Please try again later.');
    return;
  }

  try {
    loginBtn.disabled = true;
    loginBtn.textContent = 'Loading...';
    loadingMessage.style.display = 'block';

    const signInUrl = g_Clerk.buildSignInUrl({
      redirectUrl: SITE_URL,
      afterSignInUrl: SITE_URL,
      initialValues: {
        redirectUrl: SITE_URL,
      },
      origin: SITE_URL,
    });

    const tab = await chrome.tabs.create({ url: signInUrl });

    pollForAuthCompletion(tab.id);

    loginBtn.disabled = false;
    loginBtn.textContent = 'Login to BiasGuard';
    loadingMessage.style.display = 'none';
  } catch (error) {
    loginBtn.disabled = false;
    loginBtn.textContent = 'Login to BiasGuard';
    loadingMessage.style.display = 'none';
    alert('Unable to open sign in. Please try again.');
  }
};

const openSignUp = async () => {
  const signupBtn = document.getElementById('signupBtn');
  const loadingMessage = document.getElementById('loadingMessage');

  if (!g_Clerk) {
    alert('Authentication service is not available. Please try again later.');
    return;
  }

  try {
    signupBtn.disabled = true;
    signupBtn.textContent = 'Loading...';
    loadingMessage.style.display = 'block';

    const signUpUrl = g_Clerk.buildSignUpUrl({
      redirectUrl: SITE_URL,
      afterSignUpUrl: SITE_URL,
      initialValues: {
        redirectUrl: SITE_URL,
      },
      origin: SITE_URL,
    });

    const tab = await chrome.tabs.create({ url: signUpUrl });

    pollForAuthCompletion(tab.id);

    signupBtn.disabled = false;
    signupBtn.textContent = 'Create Account';
    loadingMessage.style.display = 'none';
  } catch (error) {
    signupBtn.disabled = false;
    signupBtn.textContent = 'Create Account';
    loadingMessage.style.display = 'none';
    alert('Unable to open sign up. Please try again.');
  }
};


const showLoginSection = () => {
  loginSection.style.display = 'block';
  dashboardSection.style.display = 'none';
  updateStatus('Not authenticated', '#ef4444');
};

const showDashboardSection = () => {
  loginSection.style.display = 'none';
  dashboardSection.style.display = 'block';
  updateStatus('Authenticated', '#10b981');
};

const showDashboardSectionWithoutAuth = () => {
  loginSection.style.display = 'none';
  dashboardSection.style.display = 'block';
  updateStatus('Ready', '#10b981');
  
  const userInfo = document.querySelector('.user-info');
  if (userInfo) {
    userInfo.style.display = 'none';
  }
  
  const planInfo = document.querySelector('.plan-info-bottom');
  if (planInfo) {
    planInfo.style.display = 'none';
  }
  
  const manageAccountBtn = document.getElementById('manageAccountBtn');
  if (manageAccountBtn) {
    manageAccountBtn.style.display = 'none';
  }
};

const updateStatus = (text, color) => {
  statusText.textContent = text;
  statusDot.style.backgroundColor = color;
};

const updateUserInfo = (isLoading = false) => {
  if (g_User) {
    userName.textContent = g_User.name || 'User';

    const userEmail = document.getElementById('userEmail');
    if (userEmail) {
      userEmail.textContent = g_User.email || '';
    }

    let planDisplay = isLoading ? 'Loading...' : `Plan: ${g_User.plan || 'Free'}`;

    if (!isLoading && g_User.subscription) {
      if (g_User.subscriptionIsPaused) {
        planDisplay += ' - Paused';
      } else if (g_User.subscriptionIsCancelled) {
        planDisplay += ' - Cancelled';
      }

      if (g_User.subscriptionEndDate) {
        const endDate = new Date(g_User.subscriptionEndDate);
        const formattedDate = endDate.toISOString().split('T')[0];
        planDisplay += ` - Expires at ${formattedDate}`;
      }
    }

    userPlan.textContent = planDisplay;

    const avatar = document.querySelector('.avatar');
    if (g_User.imageUrl) {
      avatar.innerHTML = `<img src="${g_User.imageUrl}" alt="User avatar" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover;">`;
    } else {
      avatar.textContent = '';
    }
  }
};

const toggleInjection = async (enabled) => {
  g_InjectionEnabled = enabled;
  try {
    await chrome.storage.local.set({ injectionEnabled: enabled });
  } catch (error) {
    console.error('Error saving injection state:', error);
  }

  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });
    if (tab) {
      if (enabled) {
        await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: window.BiasGuardUtils?.checkClerkDetection() || (() => {
            if (window.Clerk || document.querySelector('[data-clerk]') || document.querySelector('[class*="clerk"]')) {
              window.biasGuardClerkDetected = true;
            }
            return false;
          }),
        });

        await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: window.BiasGuardUtils?.setBiasGuardState(true, false) || (() => {
            window.biasGuardInjected = true;
            window.biasGuardDisabled = false;
          }),
        });

      } else {
        await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: window.BiasGuardUtils?.cleanupBiasGuard() || (() => {
            window.biasGuardDisabled = true;
            window.biasGuardInjected = false;
          }),
        });
      }
    }
  } catch (error) {
    console.error(error);
  }
};

const loadInjectionState = async () => {
  try {
    const { injectionEnabled } = await chrome.storage.local.get(['injectionEnabled']);
    g_InjectionEnabled = injectionEnabled || false;
    injectionToggle.checked = g_InjectionEnabled;
  } catch (error) {
    console.error('Error loading injection state:', error);
    g_InjectionEnabled = false;
    injectionToggle.checked = false;
  }
};

const handleAuthRedirect = async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const clerkToken = urlParams.get('__clerk_db_jwt') || urlParams.get('token');

  if (clerkToken) {
    chrome.storage.local.set({ clerkToken: clerkToken }, () => {
      showDashboardSection();
      updateUserInfo(true);

      fetchUserInfo()
        .then(() => {
          showDashboardSection();
          updateUserInfo(false);
        })
        .catch((error) => {
          showDashboardSection();
          updateUserInfo(false);
        });

      const cleanUrl = chrome.runtime.getURL('popup.html');
      window.history.replaceState({}, document.title, cleanUrl);
    });
  }
};

const pollForAuthCompletion = (tabId) => {
  let attempts = 0;
  const maxAttempts = 60;

  const checkAuth = async () => {
    attempts++;

    try {
      const tabs = await chrome.tabs.query({ tabId: tabId });
      if (tabs.length === 0) {
        return;
      }

      const tab = tabs[0];
      if (
        tab.url &&
        (tab.url.includes('localhost:3000') ||
          tab.url.includes('biasguards.ai'))
      ) {
        try {
          const results = await chrome.scripting.executeScript({
            target: { tabId: tabId },
            func: () => {
              if (
                typeof window !== 'undefined' &&
                window.Clerk &&
                window.Clerk.user
              ) {
                return {
                  authenticated: true,
                  user: {
                    id: window.Clerk.user.id,
                    name:
                      window.Clerk.user.fullName ||
                      window.Clerk.user.firstName ||
                      'User',
                    email:
                      window.Clerk.user.emailAddresses[0]?.emailAddress || '',
                    imageUrl: window.Clerk.user.imageUrl,
                  },
                };
              }
              return { authenticated: false };
            },
          });

          const result = results[0]?.result;
          if (result && result.authenticated) {
            g_User = {
              id: result.user.id,
              name: result.user.name,
              email: result.user.email,
              plan: 'Active',
              imageUrl: result.user.imageUrl,
            };

            const tokenResults = await chrome.scripting.executeScript({
              target: { tabId: tabId },
              func: async () => {
                if (window.Clerk && window.Clerk.session) {
                  return await window.Clerk.session.getToken();
                }
                return null;
              },
            });

            const token = tokenResults[0]?.result;
            if (token) {
              chrome.storage.local.set({ clerkToken: token }, () => {
                chrome.tabs.remove(tabId);

                showDashboardSection();
                updateUserInfo(true);

                fetchUserInfo()
                  .then(() => {
                    showDashboardSection();
                    updateUserInfo(false);
                  })
                  .catch((error) => {
                    showDashboardSection();
                    updateUserInfo(false);
                  });
              });
            }

            return;
          }
        } catch (error) {
          console.error(error);
        }
      }

      if (attempts < maxAttempts) {
        setTimeout(checkAuth, 500);
      } else {
        chrome.tabs.remove(tabId);
      }
    } catch (error) {
      console.error(error);
    }
  };

  setTimeout(checkAuth, 500);
};

document.addEventListener('DOMContentLoaded', async () => {
  if (!CONFIG.AUTHENTICATION_ENABLED) {
    showDashboardSectionWithoutAuth();
    await loadInjectionState();
    
    injectionToggle.addEventListener('change', (e) => {
      toggleInjection(e.target.checked);
    });
    
    return;
  }

  await handleAuthRedirect();
  await initializeClerk();
  await loadInjectionState();

  document.getElementById('loginBtn').addEventListener('click', openSignIn);
  document.getElementById('signupBtn').addEventListener('click', openSignUp);
  document.getElementById('manageAccountBtn').addEventListener('click', () => {
    if (g_Clerk && g_ClerkReady) {
      g_Clerk.openUserProfile();
    }
  });
  injectionToggle.addEventListener('change', (e) => {
    toggleInjection(e.target.checked);
  });

  await checkAuthenticationStatus();

  const authCheckInterval = setInterval(async () => {
    await checkAuthenticationStatus();
  }, 2 * 60 * 1000);

  window.addEventListener('beforeunload', () => {
    clearInterval(authCheckInterval);
  });
});

/**
 * Clean up user data and disable injection (popup version)
 */
async function cleanupUserSession() {
  g_User = null;
  g_ClerkReady = false;
  g_InjectionEnabled = false;
  injectionToggle.checked = false;
}

async function checkAuthenticationStatus() {
  try {
    const response = await chrome.runtime.sendMessage({ type: 'CHECK_AUTH_STATUS' });

    if (response.status === 'ok' && response.authResult) {
      const { isValid, needsCleanup } = response.authResult;

      if (isValid) {
        try {
          const userData = await fetchUserInfo();
          if (userData) {
            showDashboardSection();
            updateUserInfo(false);
            return { isValid: true, needsCleanup: false };
          } else {
            showLoginSection();
            return { isValid: false, needsCleanup: true };
          }
        } catch (error) {
          showLoginSection();
          return { isValid: false, needsCleanup: true };
        }
      } else {
        if (needsCleanup) {
          await cleanupUserSession();
        }
        showLoginSection();
        return { isValid: false, needsCleanup: needsCleanup };
      }
    } else {
      showLoginSection();
      return { isValid: false, needsCleanup: true };
    }
  } catch (error) {
    showLoginSection();
    return { isValid: false, needsCleanup: true };
  }
}
