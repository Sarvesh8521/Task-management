/**
 * Main Application — Initializes the SPA shell, routes, and global functions.
 */

function initApp() {
  const app = document.getElementById('app');

  // Apply theme
  const theme = localStorage.getItem('theme');
  if (theme === 'light') {
    document.documentElement.classList.add('theme-light');
  }

  // Check auth
  if (!window.api.isAuthenticated) {
    app.classList.remove('app');
    window.renderLoginPage();
    return;
  }

  // Ensure app shell layout class is applied
  app.classList.add('app');

  // Render app shell
  app.innerHTML = `
    ${window.renderSidebar()}
    <div class="main-content">
      ${window.renderHeader()}
      <div class="page-content" id="page-content">
        <div style="display:flex;align-items:center;justify-content:center;height:100%">
          <div class="spinner spinner-lg"></div>
        </div>
      </div>
    </div>
  `;

  // Init header events
  window.initHeaderEvents();

  // Register routes
  window.router.register('/dashboard', () => { window.renderDashboardPage(); window.updateTaskCount(); });
  window.router.register('/board', () => { window.renderBoardPage(); window.updateTaskCount(); });
  window.router.register('/tasks', () => { window.renderTasksPage(); window.updateTaskCount(); });
  window.router.register('/projects', () => { window.renderProjectsPage(); });
  window.router.register('/organizations', () => { window.renderOrganizationsPage(); });
  window.router.register('/users', () => { window.renderUsersPage(); });
  window.router.register('/settings', () => { window.renderSettingsPage(); });

  // Load data then start router
  window.store.loadAll().then(() => {
    window.updateTaskCount();
    window.router.start();
  });

  // Listen for data changes
  window.store.on('tasks', () => window.updateTaskCount());
}

window.generateUserDropdown = function(selectedId = null, fallbackId = null) {
  const users = window.store.get('users') || [];
  let options = '<option value="">Select a user...</option>';
  users.forEach(u => {
    const isSelected = (selectedId == u.id) || (fallbackId == u.id);
    options += `<option value="${u.id}" ${isSelected ? 'selected' : ''}>${u.first_name} ${u.last_name} (@${u.user_name})</option>`;
  });
  return options;
};

// Create Task Modal (global, used from multiple pages)
function showCreateTaskModal() {
  const projects = window.store.get('projects') || [];
  const user = window.store.get('user');

  const body = document.createElement('div');
  body.innerHTML = `
    <div class="form-group">
      <label class="form-label">Task Name</label>
      <input class="form-input" id="new-task-name" placeholder="Enter task name" required />
    </div>

    <div class="form-group">
      <label class="form-label">Description</label>
      <textarea class="form-textarea" id="new-task-desc" placeholder="Describe the task..."></textarea>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div class="form-group">
        <label class="form-label">Project</label>
        <select class="form-select" id="new-task-project">
          ${projects.length === 0
            ? '<option value="">No projects available</option>'
            : projects.map(p => `<option value="${p.id}">${p.name}</option>`).join('')
          }
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Issue Type</label>
        <select class="form-select" id="new-task-type">
          <option value="task">Task</option>
          <option value="bug">Bug</option>
          <option value="story">Story</option>
          <option value="epic">Epic</option>
          <option value="subtask">Sub-task</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Priority</label>
        <select class="form-select" id="new-task-priority">
          <option value="medium" selected>Medium</option>
          <option value="highest">Highest</option>
          <option value="high">High</option>
          <option value="low">Low</option>
          <option value="lowest">Lowest</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Status</label>
        <select class="form-select" id="new-task-status">
          <option value="todo" selected>To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="in_review">In Review</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Sprint</label>
        <input class="form-input" id="new-task-sprint" value="1" />
      </div>
      <div class="form-group">
        <label class="form-label">Assign To</label>
        <select class="form-input form-select" id="new-task-user" required>
          ${window.generateUserDropdown(null, window.store.get('user')?.id)}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Start Date</label>
        <input class="form-input" type="date" id="new-task-start" />
      </div>
      <div class="form-group">
        <label class="form-label">End Date</label>
        <input class="form-input" type="date" id="new-task-end" />
      </div>
    </div>
  `;

  const footer = document.createElement('div');
  footer.style.cssText = 'display:flex;gap:12px;justify-content:flex-end;width:100%';
  footer.innerHTML = `
    <button class="btn btn-secondary" onclick="Modal.close()">Cancel</button>
    <button class="btn btn-primary" id="save-new-task">Create Task</button>
  `;

  Modal.open({ title: 'Create New Task', body, footer, wide: true });

  footer.querySelector('#save-new-task').addEventListener('click', async () => {
    const name = document.getElementById('new-task-name').value.trim();
    const projectVal = document.getElementById('new-task-project').value;
    if (!name) { window.toast.warning('Task name is required'); return; }
    if (!projectVal) { window.toast.warning('Please select a project'); return; }

    try {
      await window.api.createTask({
        name,
        description: document.getElementById('new-task-desc').value,
        project: parseInt(projectVal),
        users: parseInt(document.getElementById('new-task-user').value),
        issue_type: document.getElementById('new-task-type').value,
        priority: document.getElementById('new-task-priority').value,
        status: document.getElementById('new-task-status').value,
        sprint: document.getElementById('new-task-sprint').value,
        start_date: document.getElementById('new-task-start').value || null,
        end_date: document.getElementById('new-task-end').value || null,
      });
      Modal.close();
      window.toast.success('Task created!');
      await window.store.loadTasks();
      // Re-render current page
      const route = window.router.current;
      if (route) window.router.navigate(route);
    } catch (err) {
      window.toast.error(err.message);
    }
  });
}

window.showCreateTaskModal = showCreateTaskModal;

// Auth logout handler
window.addEventListener('auth:logout', () => {
  const app = document.getElementById('app');
  if (app) app.classList.remove('app');
  window.renderLoginPage();
});

// Boot
document.addEventListener('DOMContentLoaded', initApp);
