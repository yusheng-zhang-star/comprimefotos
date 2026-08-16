/**
 * Adsterra Ad Loader — standard banner units only (no Native Banner).
 * Banner slots are initialised sequentially with a small delay to
 * avoid atOptions collisions between multiple banner units.
 */
(function () {
  'use strict';

  var mobileQuery = window.matchMedia ? window.matchMedia('(max-width: 767px)') : null;

  var TOP_DESKTOP = {
    key: '3137dc254843fa13f927ed16c5d86dc2',
    width: 728,
    height: 90
  };

  var TOP_MOBILE = {
    key: '560c7e1256c3e9643ffec382497532f8',
    width: 320,
    height: 50
  };

  var CONTENT_AD = {
    key: 'b099a20b28b1815e84079ea60d45a326',
    width: 300,
    height: 250
  };

  function isMobile() {
    return mobileQuery ? mobileQuery.matches : false;
  }

  function loadAtOptionsAd(container, unit) {
    if (!container || !unit) return;

    var optionsScript = document.createElement('script');
    optionsScript.text = 'atOptions = ' + JSON.stringify({
      key: unit.key,
      format: 'iframe',
      height: unit.height,
      width: unit.width,
      params: {}
    }) + ';';
    container.appendChild(optionsScript);

    var script = document.createElement('script');
    script.src = 'https://www.highperformanceformat.com/' + unit.key + '/invoke.js';
    container.appendChild(script);
  }

  function initTopAd() {
    var header = document.querySelector('.site-header') || document.querySelector('header');
    if (!header) return;

    var container = document.createElement('div');
    container.className = 'ad-slot ad-top';

    if (isMobile()) {
      container.classList.add('ad-top-mobile');
      header.after(container);
      loadAtOptionsAd(container, TOP_MOBILE);
    } else {
      container.classList.add('ad-top-desktop');
      header.after(container);
      loadAtOptionsAd(container, TOP_DESKTOP);
    }
  }

  function initContentAd() {
    if (isMobile()) return;

    var isToolPage = /\/tools\//.test(window.location.pathname) ||
      !!document.querySelector('.tool-page, .tool-workspace');
    if (!isToolPage) return;

    var anchor = document.querySelector(
      '#downloadBtn, #downloadButton, [id*="download" i], .download-section, ' +
      '#resultSection, .result-section, #previewSection, .preview-box, #previewBox, #previewCanvas'
    );

    var container = document.createElement('div');
    container.className = 'ad-slot ad-content';

    if (anchor) {
      var wrapper = anchor.closest('.tool-result, .result-box, .tool-panel, .tool-workspace, .card, section') ||
        anchor.parentElement;
      if (wrapper && wrapper !== document.body) {
        wrapper.after(container);
      } else {
        anchor.after(container);
      }
    } else {
      var main = document.querySelector('main');
      if (main) main.appendChild(container);
      else document.body.appendChild(container);
    }

    loadAtOptionsAd(container, CONTENT_AD);
  }

  function initFooterAd() {
    var footer = document.querySelector('.site-footer') || document.querySelector('footer');
    if (!footer) return;

    var container = document.createElement('div');
    container.className = 'ad-slot ad-footer';

    if (isMobile()) {
      container.classList.add('ad-top-mobile');
    } else {
      container.classList.add('ad-top-desktop');
    }

    footer.before(container);
    loadAtOptionsAd(container, isMobile() ? TOP_MOBILE : TOP_DESKTOP);
  }

  function init() {
    var steps = [initTopAd, initContentAd, initFooterAd];
    var index = 0;
    function next() {
      if (index >= steps.length) return;
      try { steps[index](); } catch (e) {}
      index += 1;
      setTimeout(next, 150);
    }
    next();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
