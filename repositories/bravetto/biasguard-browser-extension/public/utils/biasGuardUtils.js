(function() {
  'use strict';

  window.BiasGuardUtils = {
    cleanupBiasGuard: function() {
      const highlights = document.querySelectorAll('.biasguard-highlight');
      highlights.forEach(highlight => {
        const parent = highlight.parentNode;
        if (parent) {
          parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
          parent.normalize();
        }
      });

      const notification = document.getElementById('biasguard-notification');
      if (notification) {
        notification.remove();
      }

      const modal = document.getElementById('biasguard-modal');
      if (modal) {
        modal.remove();
      }

      const styles = document.getElementById('biasguard-styles');
      if (styles) {
        styles.remove();
      }

      window.biasGuardInjected = false;
      window.biasGuardDisabled = true;
    },

    isEnabled: function() {
      return window.biasGuardInjected && !window.biasGuardDisabled;
    },

    addStyles: function() {
      if (document.getElementById('biasguard-styles')) return;

      const style = document.createElement('style');
      style.id = 'biasguard-styles';
      style.textContent = `
        .biasguard-highlight {
          background: linear-gradient(120deg, #ff6b6b 0%, #ff8e8e 100%);
          color: white;
          padding: 1px 3px;
          border-radius: 3px;
          font-weight: bold;
          cursor: help;
          transition: all 0.2s ease;
          box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }

        .biasguard-highlight:hover {
          background: linear-gradient(120deg, #ff5252 0%, #ff7979 100%);
          transform: scale(1.05);
          box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        }

        .biasguard-critical {
          background: linear-gradient(120deg, #dc3545 0%, #e74c3c 100%);
        }

        .biasguard-high {
          background: linear-gradient(120deg, #fd7e14 0%, #ff9f43 100%);
        }

        .biasguard-medium {
          background: linear-gradient(120deg, #ffc107 0%, #ffd43b 100%);
          color: #333;
        }

        .biasguard-low {
          background: linear-gradient(120deg, #28a745 0%, #20c997 100%);
        }

        #biasguard-notification {
          animation: slideIn 0.3s ease-out;
        }

        @keyframes slideIn {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
      `;

      document.head.appendChild(style);
    }
  };

  window.BiasGuardUtils.addStyles();
})();
