/**
 * Modal Component
 */
class Modal {
  static open({ title, body, footer, wide = false }) {
    Modal.close(); // close any existing

    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop';
    backdrop.id = 'modal-backdrop';

    const modalEl = document.createElement('div');
    modalEl.className = 'modal fade-in';
    if (wide) modalEl.style.maxWidth = '720px';

    modalEl.innerHTML = `
      <div class="modal-header">
        <h3 class="modal-title">${title}</h3>
        <button class="modal-close" id="modal-close-btn">✕</button>
      </div>
      <div class="modal-body" id="modal-body"></div>
      ${footer ? `<div class="modal-footer" id="modal-footer"></div>` : ''}
    `;

    backdrop.appendChild(modalEl);
    document.body.appendChild(backdrop);

    const bodyEl = modalEl.querySelector('#modal-body');
    if (typeof body === 'string') {
      bodyEl.innerHTML = body;
    } else if (body instanceof HTMLElement) {
      bodyEl.appendChild(body);
    }

    if (footer) {
      const footerEl = modalEl.querySelector('#modal-footer');
      if (typeof footer === 'string') {
        footerEl.innerHTML = footer;
      } else if (footer instanceof HTMLElement) {
        footerEl.appendChild(footer);
      }
    }

    // Close handlers
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) Modal.close();
    });
    modalEl.querySelector('#modal-close-btn').addEventListener('click', Modal.close);
    document.addEventListener('keydown', Modal._onKeyDown);

    return modalEl;
  }

  static close() {
    const backdrop = document.getElementById('modal-backdrop');
    if (backdrop) backdrop.remove();
    document.removeEventListener('keydown', Modal._onKeyDown);
  }

  static _onKeyDown(e) {
    if (e.key === 'Escape') Modal.close();
  }

  /**
   * Convenience: Confirm dialog
   */
  static confirm(message) {
    return new Promise((resolve) => {
      const footer = document.createElement('div');
      footer.style.cssText = 'display:flex;gap:12px;justify-content:flex-end;width:100%';
      footer.innerHTML = `
        <button class="btn btn-secondary" id="modal-cancel">Cancel</button>
        <button class="btn btn-danger" id="modal-confirm">Confirm</button>
      `;

      Modal.open({
        title: 'Confirm Action',
        body: `<p style="color:var(--color-text-secondary)">${message}</p>`,
        footer,
      });

      footer.querySelector('#modal-cancel').addEventListener('click', () => { Modal.close(); resolve(false); });
      footer.querySelector('#modal-confirm').addEventListener('click', () => { Modal.close(); resolve(true); });
    });
  }
}

window.Modal = Modal;
