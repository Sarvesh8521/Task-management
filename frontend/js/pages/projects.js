/**
 * Projects Page
 */
function renderProjectsPage() {
  window.updateHeaderTitle('Projects');

  const page = document.getElementById('page-content');
  const projects = window.store.get('projects') || [];
  const tasks = window.store.get('tasks') || [];

  page.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">Projects</h1>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="showCreateProjectModal()">+ New Project</button>
      </div>
    </div>

    ${projects.length === 0 ? `
      <div class="empty-state">
        <div class="empty-state-icon">📁</div>
        <div class="empty-state-title">No projects yet</div>
        <div class="empty-state-text">Create your first project to organize tasks</div>
        <button class="btn btn-primary" onclick="showCreateProjectModal()" style="margin-top:16px">+ Create Project</button>
      </div>
    ` : `
      <div class="projects-grid">
        ${projects.map(project => {
          const projectTasks = tasks.filter(t => t.project === project.id);
          const completedTasks = projectTasks.filter(t => t.status === 'completed').length;
          const statusLabel = project.status ? project.status.replace('_', ' ') : 'planned';
          return `
            <div class="project-card slide-up" onclick='showProjectDetail(${JSON.stringify(project).replace(/'/g, "&#39;")})'>
              <div class="project-card-header">
                <div>
                  <div class="project-card-name">${project.name}</div>
                  <span class="badge badge-${project.status || 'planned'}" style="margin-top:8px">${statusLabel}</span>
                </div>
                <button class="btn btn-ghost btn-sm" onclick="event.stopPropagation(); deleteProjectItem(${project.id})" title="Delete">🗑</button>
              </div>
              <div class="project-card-meta">
                <div class="project-card-stat">
                  <div class="project-card-stat-value">${projectTasks.length}</div>
                  <div class="project-card-stat-label">Tasks</div>
                </div>
                <div class="project-card-stat">
                  <div class="project-card-stat-value">${completedTasks}</div>
                  <div class="project-card-stat-label">Done</div>
                </div>
                <div class="project-card-stat">
                  <div class="project-card-stat-value">${project.sprint || 1}</div>
                  <div class="project-card-stat-label">Sprint</div>
                </div>
              </div>
            </div>
          `;
        }).join('')}
      </div>
    `}
  `;
}

function showCreateProjectModal() {
  const user = window.store.get('user');
  const body = document.createElement('div');
  body.innerHTML = `
    <div class="form-group">
      <label class="form-label">Project Name</label>
      <input class="form-input" id="new-project-name" placeholder="Enter project name" required />
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div class="form-group">
        <label class="form-label">Status</label>
        <select class="form-select" id="new-project-status">
          <option value="planned">Planned</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
          <option value="on_hold">On Hold</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Sprint</label>
        <input class="form-input" type="number" id="new-project-sprint" value="1" min="1" />
      </div>
      <div class="form-group">
        <label class="form-label">Start Date</label>
        <input class="form-input" type="date" id="new-project-start" />
      </div>
      <div class="form-group">
        <label class="form-label">End Date</label>
        <input class="form-input" type="date" id="new-project-end" />
      </div>
      <div class="form-group">
        <label class="form-label">Super User</label>
        <select class="form-input form-select" id="new-proj-super" required>
          ${window.generateUserDropdown(null, user?.id)}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Sub User</label>
        <select class="form-input form-select" id="new-proj-sub">
          <option value="">None</option>
          ${window.generateUserDropdown(null, user?.id)}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Assigned User</label>
        <select class="form-input form-select" id="new-proj-user" required>
          ${window.generateUserDropdown(null, user?.id)}
        </select>
      </div>
    </div>
  `;

  const footer = document.createElement('div');
  footer.style.cssText = 'display:flex;gap:12px;justify-content:flex-end;width:100%';
  footer.innerHTML = `
    <button class="btn btn-secondary" onclick="Modal.close()">Cancel</button>
    <button class="btn btn-primary" id="save-new-project">Create Project</button>
  `;

  Modal.open({ title: 'Create New Project', body, footer });

  footer.querySelector('#save-new-project').addEventListener('click', async () => {
    const name = document.getElementById('new-project-name').value.trim();
    if (!name) { window.toast.warning('Project name is required'); return; }

    try {
      await window.api.createProject({
        name,
        status: document.getElementById('new-project-status').value,
        sprint: parseInt(document.getElementById('new-project-sprint').value) || 1,
        start_date: document.getElementById('new-project-start').value || null,
        end_date: document.getElementById('new-project-end').value || null,
        super_user: parseInt(document.getElementById('new-proj-super').value) || null,
        sub_user: parseInt(document.getElementById('new-proj-sub').value) || null,
        user: parseInt(document.getElementById('new-proj-user').value) || null,
      });
      Modal.close();
      window.toast.success('Project created!');
      await window.store.loadProjects();
      renderProjectsPage();
    } catch (err) {
      window.toast.error(err.message);
    }
  });
}

function showProjectDetail(project) {
  const tasks = (window.store.get('tasks') || []).filter(t => t.project === project.id);
  const body = document.createElement('div');
  body.innerHTML = `
    <div class="form-group">
      <label class="form-label">Project Name</label>
      <input class="form-input" id="edit-project-name" value="${project.name}" />
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div class="form-group">
        <label class="form-label">Status</label>
        <select class="form-select" id="edit-project-status">
          ${['planned','in_progress','completed','on_hold','cancelled'].map(s =>
            `<option value="${s}" ${s === project.status ? 'selected' : ''}>${s.replace('_', ' ')}</option>`
          ).join('')}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Sprint</label>
        <input class="form-input" type="number" id="edit-project-sprint" value="${project.sprint || 1}" min="1" />
      </div>
      <div class="form-group">
        <label class="form-label">Super User</label>
        <select class="form-input form-select" id="edit-proj-super">
          ${window.generateUserDropdown(project.super_user)}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Sub User</label>
        <select class="form-input form-select" id="edit-proj-sub">
          <option value="">None</option>
          ${window.generateUserDropdown(project.sub_user)}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Assigned User</label>
        <select class="form-input form-select" id="edit-proj-user">
          ${window.generateUserDropdown(project.user)}
        </select>
      </div>
    </div>
    <div style="margin-top:16px">
      <label class="form-label">Project Tasks (${tasks.length})</label>
      <div style="max-height:200px;overflow-y:auto;margin-top:8px;">
        ${tasks.length === 0 ? '<p style="color:var(--color-text-tertiary);font-size:13px">No tasks in this project</p>' :
          tasks.map(t => `
            <div class="recent-task-item" style="margin-bottom:4px">
              <span class="badge badge-${t.issue_type}" style="font-size:10px">${t.issue_type}</span>
              <span class="truncate" style="flex:1">${t.name}</span>
              <span class="badge badge-${t.status}">${t.status.replace('_', ' ')}</span>
            </div>
          `).join('')}
      </div>
    </div>
  `;

  const footer = document.createElement('div');
  footer.style.cssText = 'display:flex;gap:12px;justify-content:flex-end;width:100%';
  footer.innerHTML = `
    <button class="btn btn-secondary" onclick="Modal.close()">Cancel</button>
    <button class="btn btn-primary" id="save-edit-project">Save</button>
  `;

  Modal.open({ title: project.name, body, footer, wide: true });

  footer.querySelector('#save-edit-project').addEventListener('click', async () => {
    try {
      await window.api.updateProject(project.id, {
        name: document.getElementById('edit-project-name').value,
        status: document.getElementById('edit-project-status').value,
        sprint: parseInt(document.getElementById('edit-project-sprint').value) || 1,
        super_user: parseInt(document.getElementById('edit-proj-super').value) || null,
        sub_user: parseInt(document.getElementById('edit-proj-sub').value) || null,
        user: parseInt(document.getElementById('edit-proj-user').value) || null,
      });
      Modal.close();
      window.toast.success('Project updated');
      await window.store.loadProjects();
      renderProjectsPage();
    } catch (err) {
      window.toast.error(err.message);
    }
  });
}

async function deleteProjectItem(projectId) {
  const confirmed = await Modal.confirm('Are you sure you want to delete this project?');
  if (confirmed) {
    try {
      await window.api.deleteProject(projectId);
      window.toast.success('Project deleted');
      await window.store.loadProjects();
      renderProjectsPage();
    } catch (err) {
      window.toast.error(err.message);
    }
  }
}

window.renderProjectsPage = renderProjectsPage;
window.showCreateProjectModal = showCreateProjectModal;
window.showProjectDetail = showProjectDetail;
window.deleteProjectItem = deleteProjectItem;
