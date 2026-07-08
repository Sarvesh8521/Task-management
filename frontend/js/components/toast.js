/**
 * Toast Notification System
 */
class ToastManager {
  constructor() {
    this._container = document.createElement('div');
    this._container.className = 'toast-container';
    this._container.id = 'toast-container';
    document.body.appendChild(this._container);
  }

  _show(message, type = 'info', duration = 4000) {
    const icons = { success: '✓', error: '✕', warning: '⚠', info: 'ℹ' };
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <span class="toast-icon">${icons[type] || icons.info}</span>
      <span class="toast-message">${message}</span>
      <button class="toast-close" onclick="this.closest('.toast').remove()">✕</button>
    `;
    this._container.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('toast-exit');
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }

  success(msg) { this._show(msg, 'success'); }
  error(msg) { this._show(msg, 'error', 6000); }
  warning(msg) { this._show(msg, 'warning'); }
  info(msg) { this._show(msg, 'info'); }
}

window.toast = new ToastManager();
