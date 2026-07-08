/**
 * Organizations Page
 */
function renderOrganizationsPage() {
  window.updateHeaderTitle('Organizations');
  const page = document.getElementById('page-content');
  const user = window.store.get('user');

  page.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">Organizations</h1>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="showCreateOrgModal()">+ New Organization</button>
      </div>
    </div>

    <div class="card slide-up" id="org-content">
      <div class="empty-state" style="padding:48px">
        <div class="empty-state-icon">🏢</div>
        <div class="empty-state-title">Manage your organizations</div>
        <div class="empty-state-text">Search by ID to view or edit an organization</div>
      </div>

      <div style="margin-top:24px;display:flex;gap:12px;align-items:flex-end;justify-content:center">
        <div class="form-group" style="width:200px">
          <label class="form-label">Organization ID</label>
          <input class="form-input" type="number" id="org-search-id" placeholder="Enter ID" min="1" />
        </div>
        <button class="btn btn-primary" onclick="searchOrg()" style="height:38px">Search</button>
      </div>

      <div id="org-result" style="margin-top:24px"></div>
    </div>
  `;
}

async function searchOrg() {
  const id = document.getElementById('org-search-id').value;
  if (!id) { window.toast.warning('Enter an organization ID'); return; }

  const resultEl = document.getElementById('org-result');
  resultEl.innerHTML = '<div style="text-align:center;padding:16px"><div class="spinner spinner-lg" style="margin:0 auto"></div></div>';

  try {
    const org = await window.api.getOrganization(id);
    resultEl.innerHTML = `
      <div class="card" style="border-color:var(--color-primary);border-width:1px;">
        <div class="card-header">
          <div>
            <div class="card-title">${org.name}</div>
            <div style="font-size:12px;color:var(--color-text-tertiary);margin-top:4px">ID: ${org.id} • Created: ${new Date(org.creation_date).toLocaleDateString()}</div>
          </div>
          <div style="display:flex;gap:8px">
            <button class="btn btn-secondary btn-sm" onclick='showEditOrgModal(${JSON.stringify(org).replace(/'/g, "&#39;")})'>Edit</button>
            <button class="btn btn-danger btn-sm" onclick="deleteOrg(${org.id})">Delete</button>
          </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:8px">
          <div class="form-group">
            <span class="form-label">Super User</span>
            <span style="font-weight:500">#${org.super_user}</span>
          </div>
          <div class="form-group">
            <span class="form-label">Sub User</span>
            <span style="font-weight:500">#${org.sub_user}</span>
          </div>
        </div>
      </div>
    `;
  } catch (err) {
    resultEl.innerHTML = `<div class="login-error">${err.message}</div>`;
  }
}

function showCreateOrgModal() {
  const user = window.store.get('user');
  const body = document.createElement('div');
  body.innerHTML = `
    <div class="form-group">
      <label class="form-label">Organization Name</label>
      <input class="form-input" id="new-org-name" placeholder="Enter name" required />
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div class="form-group">
        <label class="form-label">Super User</label>
        <select class="form-input form-select" id="new-org-super" required>
          ${window.generateUserDropdown(null, user?.id)}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Sub User</label>
        <select class="form-input form-select" id="new-org-sub">
          <option value="">None</option>
          ${window.generateUserDropdown(null, user?.id)}
        </select>
      </div>
    </div>
  `;

  const footer = document.createElement('div');
  footer.style.cssText = 'display:flex;gap:12px;justify-content:flex-end;width:100%';
  footer.innerHTML = `
    <button class="btn btn-secondary" onclick="Modal.close()">Cancel</button>
    <button class="btn btn-primary" id="save-new-org">Create</button>
  `;

  Modal.open({ title: 'Create Organization', body, footer });

  footer.querySelector('#save-new-org').addEventListener('click', async () => {
    const name = document.getElementById('new-org-name').value.trim();
    if (!name) { window.toast.warning('Name is required'); return; }
    try {
      await window.api.createOrganization({
        name,
        super_user: parseInt(document.getElementById('new-org-super').value) || null,
        sub_user: parseInt(document.getElementById('new-org-sub').value) || null,
      });
      Modal.close();
      window.toast.success('Organization created!');
    } catch (err) {
      window.toast.error(err.message);
    }
  });
}

function showEditOrgModal(org) {
  const body = document.createElement('div');
  body.innerHTML = `
    <div class="form-group">
      <label class="form-label">Organization Name</label>
      <input class="form-input" id="edit-org-name" value="${org.name}" />
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div class="form-group">
        <label class="form-label">Super User</label>
        <select class="form-input form-select" id="edit-org-super">
          ${window.generateUserDropdown(org.super_user)}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Sub User</label>
        <select class="form-input form-select" id="edit-org-sub">
          <option value="">None</option>
          ${window.generateUserDropdown(org.sub_user)}
        </select>
      </div>
    </div>
  `;

  const footer = document.createElement('div');
  footer.style.cssText = 'display:flex;gap:12px;justify-content:flex-end;width:100%';
  footer.innerHTML = `
    <button class="btn btn-secondary" onclick="Modal.close()">Cancel</button>
    <button class="btn btn-primary" id="save-edit-org">Save</button>
  `;

  Modal.open({ title: `Edit: ${org.name}`, body, footer });

  footer.querySelector('#save-edit-org').addEventListener('click', async () => {
    try {
      await window.api.updateOrganization(org.id, {
        name: document.getElementById('edit-org-name').value,
        super_user: parseInt(document.getElementById('edit-org-super').value) || null,
        sub_user: parseInt(document.getElementById('edit-org-sub').value) || null,
      });
      Modal.close();
      window.toast.success('Organization updated');
      searchOrg();
    } catch (err) {
      window.toast.error(err.message);
    }
  });
}

async function deleteOrg(orgId) {
  const confirmed = await Modal.confirm('Delete this organization?');
  if (confirmed) {
    try {
      await window.api.deleteOrganization(orgId);
      window.toast.success('Organization deleted');
      document.getElementById('org-result').innerHTML = '';
    } catch (err) {
      window.toast.error(err.message);
    }
  }
}

window.renderOrganizationsPage = renderOrganizationsPage;
window.showCreateOrgModal = showCreateOrgModal;
window.showEditOrgModal = showEditOrgModal;
window.searchOrg = searchOrg;
window.deleteOrg = deleteOrg;
