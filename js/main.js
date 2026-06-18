/**
 * ComprimeFotos.com — JavaScript principal (v2)
 * Funciones: Menú móvil, FAQ acordeón, consentimiento cookies, dropzone
 * 
 * DIFERENCIAS con smartimgkit:
 * - Sin theme toggle (solo modo claro)
 * - Sin localStorage para tema
 * - Sin sample-image-btn
 */

document.addEventListener('DOMContentLoaded', function() {
  initMobileMenu();
  initFAQ();
  initCookieConsent();
  initContactForm();
  initDropzones();
});

/* ===== Mobile Menu ===== */
function initMobileMenu() {
  const btn = document.getElementById('mobileMenuBtn');
  const nav = document.querySelector('.main-nav');
  if (!btn || !nav) return;

  btn.addEventListener('click', function() {
    const isOpen = nav.classList.contains('nav-open');
    nav.classList.toggle('nav-open');
    btn.textContent = isOpen ? '☰' : '✕';
  });

  document.addEventListener('click', function(e) {
    if (nav.classList.contains('nav-open') && 
        !nav.contains(e.target) && 
        !btn.contains(e.target)) {
      nav.classList.remove('nav-open');
      btn.textContent = '☰';
    }
  });
}

/* ===== FAQ Accordions ===== */
function initFAQ() {
  document.querySelectorAll('.faq-question').forEach(function(btn) {
    btn.setAttribute('role', 'button');
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('tabindex', '0');

    function toggleFaq() {
      const item = btn.closest('.faq-item');
      const wasOpen = item.classList.contains('open');
      item.parentElement.querySelectorAll('.faq-item').forEach(function(i) {
        i.classList.remove('open');
        i.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
      });
      if (!wasOpen) {
        item.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
      }
    }

    btn.addEventListener('click', toggleFaq);
    btn.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleFaq();
      }
    });
  });
}

/* ===== Cookie Consent ===== */
function initCookieConsent() {
  const banner = document.getElementById('cookieConsent');
  if (!banner) return;

  try {
    if (localStorage.getItem('cf-cookies-v2')) return;
  } catch(e) { return; }

  setTimeout(function() {
    banner.classList.add('visible');
  }, 800);

  const acceptBtn = document.getElementById('cookieAccept');
  const declineBtn = document.getElementById('cookieDecline');

  if (acceptBtn) {
    acceptBtn.addEventListener('click', function() {
      try { localStorage.setItem('cf-cookies-v2', 'all'); } catch(e) {}
      banner.classList.remove('visible');
    });
  }

  if (declineBtn) {
    declineBtn.addEventListener('click', function() {
      try { localStorage.setItem('cf-cookies-v2', 'essential'); } catch(e) {}
      banner.classList.remove('visible');
    });
  }
}

/* ===== Dropzones ===== */
function initDropzones() {
  document.querySelectorAll('.dropzone').forEach(function(dropzone) {
    const fileInput = dropzone.querySelector('input[type="file"]');
    if (!fileInput) return;

    // No need for manual click() — <label for="fileInput"> handles this natively.
    // Adding fileInput.click() here causes double-triggering, requiring users
    // to click twice before the file picker actually opens.

    dropzone.addEventListener('dragover', function(e) {
      e.preventDefault();
      dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', function(e) {
      e.preventDefault();
      dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', function(e) {
      e.preventDefault();
      dropzone.classList.remove('dragover');
      if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        fileInput.dispatchEvent(new Event('change'));
      }
    });

    fileInput.addEventListener('change', function(e) {
      if (this.files && this.files.length > 0) {
        // Para múltiples archivos (batch)
        if (this.multiple && this.files.length > 1) {
          handleMultipleFiles(this.files, dropzone);
        } else {
          handleFileSelected(this.files[0], dropzone);
        }
      }
    });
  });
}

/* ===== File Selected ===== */
function handleFileSelected(file, dropzone) {
  const toolWorkspace = dropzone.closest('.tool-workspace');
  if (!toolWorkspace) return;

  const previewArea = toolWorkspace.querySelector('.preview-area');
  const previewImg = toolWorkspace.querySelector('.preview-img');
  const fileName = toolWorkspace.querySelector('.file-name');
  const fileSize = toolWorkspace.querySelector('.file-size');

  if (fileName) fileName.textContent = file.name;
  if (fileSize) fileSize.textContent = formatSize(file.size);

  if (file.type.startsWith('image/') && previewImg) {
    const reader = new FileReader();
    reader.onload = function(e) {
      previewImg.src = e.target.result;
      if (previewArea) previewArea.classList.add('active');
      dropzone.style.display = 'none';
    };
    reader.readAsDataURL(file);
  } else {
    if (previewArea) previewArea.classList.add('active');
    dropzone.style.display = 'none';
  }

  const event = new CustomEvent('file-selected', { detail: { file: file } });
  toolWorkspace.dispatchEvent(event);
}

/* ===== Multiple Files (batch) ===== */
function handleMultipleFiles(files, dropzone) {
  const toolWorkspace = dropzone.closest('.tool-workspace');
  if (!toolWorkspace) return;

  const event = new CustomEvent('files-selected', { detail: { files: files } });
  toolWorkspace.dispatchEvent(event);
}

/* ===== Contact Form ===== */
function initContactForm() {
  var form = document.querySelector('.contact-form form');
  if (!form) return;

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    var status = form.querySelector('.form-status');
    var submitBtn = form.querySelector('.form-submit');
    var original = submitBtn ? submitBtn.textContent : '';

    if (submitBtn) { submitBtn.textContent = 'Enviando...'; submitBtn.disabled = true; }
    if (status) { status.className = 'form-status'; status.textContent = ''; status.style.display = 'none'; }

    var formData = new FormData(form);

    fetch('/api/contact', { method: 'POST', body: formData })
      .then(function(resp) { return resp.json(); })
      .then(function(data) {
        if (data.success) {
          if (status) {
            status.className = 'form-status success';
            status.textContent = '¡Gracias! Te responderemos pronto.';
            status.style.display = 'block';
          }
          form.reset();
        } else {
          if (status) {
            status.className = 'form-status error';
            status.textContent = data.message || 'Error al enviar. Intenta de nuevo.';
            status.style.display = 'block';
          }
        }
      })
      .catch(function() {
        if (status) {
          status.className = 'form-status error';
          status.textContent = 'Error de conexión. Intenta de nuevo más tarde.';
          status.style.display = 'block';
        }
      })
      .then(function() {
        if (submitBtn) { submitBtn.textContent = original; submitBtn.disabled = false; }
      });
  });
}

/* ===== Utilities ===== */
function showToast(message, type) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = message;
  toast.className = 'toast';
  if (type) toast.classList.add(type);
  toast.classList.add('visible');
  setTimeout(function() { toast.classList.remove('visible'); }, 3000);
}

function formatSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
