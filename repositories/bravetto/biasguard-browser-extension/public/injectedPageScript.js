(function () {
  console.log('BiasGuard page script loaded');
  
  const script = document.createElement('script');
  script.src = chrome.runtime.getURL('bias-detect-script.js');
  script.onload = function() {
    console.log('Enhanced bias detection script loaded');
  };
  (document.head || document.documentElement).appendChild(script);
})();
