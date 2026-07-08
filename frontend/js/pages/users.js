/**
 * Users Management Page
 */
function renderUsersPage() {
  window.updateHeaderTitle('Users');
  const page = document.getElementById('page-content');
  const users = window.store.get('users') || [];

  page.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">Users</h1>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="showCreateUserModal()">+ New User</button>
      </div>
    </div>

    ${users.length === 0 ? `
      <div class="empty-state slide-up">
        <div class="empty-state-icon">👥</div>
        <div class="empty-state-title">No users found</div>
        <div class="empty-state-text">There are no users to display.</div>
      </div>
    ` : `
      <div class="card slide-up" style="padding:0; overflow:hidden">
        <table style="width:100%; border-collapse:collapse; text-align:left;">
          <thead>
            <tr style="border-bottom:1px solid var(--border-color); background:var(--color-bg-tertiary);">
              <th style="padding:16px; font-weight:600; font-size:12px; color:var(--color-text-secondary); text-transform:uppercase;">User</th>
              <th style="padding:16px; font-weight:600; font-size:12px; color:var(--color-text-secondary); text-transform:uppercase;">Email</th>
              <th style="padding:16px; font-weight:600; font-size:12px; color:var(--color-text-secondary); text-transform:uppercase;">ID</th>
              <th style="padding:16px; font-weight:600; font-size:12px; color:var(--color-text-secondary); text-transform:uppercase;">Status</th>
            </tr>
          </thead>
          <tbody>
            ${users.map(u => `
              <tr style="border-bottom:1px solid var(--border-color); transition:background var(--transition-fast);" onmouseover="this.style.background='var(--color-bg-hover)'" onmouseout="this.style.background='transparent'">
                <td style="padding:16px;">
                  <div style="display:flex; align-items:center; gap:12px;">
                    <div class="avatar" style="background:var(--color-primary); color:white; font-size:12px; display:flex; align-items:center; justify-content:center; width:32px; height:32px; border-radius:50%;">
                      ${(u.first_name?.[0] || 'U').toUpperCase()}${(u.last_name?.[0] || '').toUpperCase()}
                    </div>
                    <div>
                      <div style="font-weight:500;">${u.first_name} ${u.last_name}</div>
                      <div style="font-size:12px; color:var(--color-text-tertiary);">@${u.user_name}</div>
                    </div>
                  </div>
                </td>
                <td style="padding:16px; color:var(--color-text-secondary);">${u.email_id}</td>
                <td style="padding:16px; color:var(--color-text-tertiary);">${u.id}</td>
                <td style="padding:16px;">
                  <span class="badge badge-completed" style="background:var(--color-success-muted);color:var(--color-success)">Active</span>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `}
  `;
}

function showCreateUserModal() {
  const body = document.createElement('div');
  body.innerHTML = `
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
      <div class="form-group">
        <label class="form-label">First Name</label>
        <input class="form-input" type="text" id="new-usr-first" placeholder="Jane" required />
      </div>
      <div class="form-group">
        <label class="form-label">Last Name</label>
        <input class="form-input" type="text" id="new-usr-last" placeholder="Doe" required />
      </div>
    </div>
    <div class="form-group">
      <label class="form-label">Username</label>
      <input class="form-input" type="text" id="new-usr-username" placeholder="Choose a username" required />
    </div>
    <div class="form-group">
      <label class="form-label">Email</label>
      <input class="form-input" type="email" id="new-usr-email" placeholder="jane@example.com" required />
    </div>
    <div class="form-group">
      <label class="form-label">Temporary Password</label>
      <input class="form-input" type="password" id="new-usr-password" placeholder="Min 8 chars, 1 uppercase, 1 special char" required />
    </div>
  `;

  const footer = document.createElement('div');
  footer.style.cssText = 'display:flex;gap:12px;justify-content:flex-end;width:100%';
  footer.innerHTML = `
    <button class="btn btn-secondary" onclick="Modal.close()">Cancel</button>
    <button class="btn btn-primary" id="save-new-user">Create User</button>
  `;

  Modal.open({ title: 'Create New User', body, footer });

  footer.querySelector('#save-new-user').addEventListener('click', async () => {
    try {
      await window.api.createUser({
        user_name: document.getElementById('new-usr-username').value.trim(),
        email_id: document.getElementById('new-usr-email').value.trim(),
        password: document.getElementById('new-usr-password').value,
        first_name: document.getElementById('new-usr-first').value.trim(),
        last_name: document.getElementById('new-usr-last').value.trim(),
      });
      Modal.close();
      window.toast.success('User created successfully!');
      await window.store.loadUsers();
      renderUsersPage();
    } catch (err) {
      window.toast.error(err.message || 'Failed to create user');
    }
  });
}

window.renderUsersPage = renderUsersPage;
window.showCreateUserModal = showCreateUserModal;
