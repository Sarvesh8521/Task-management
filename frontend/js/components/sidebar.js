/**
 * Sidebar Navigation Component
 */
function renderSidebar() {
  const user = window.store.get('user');
  const initials = user ? (user.first_name?.[0] || '') + (user.last_name?.[0] || '') : 'U';
  const displayName = user ? `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.username : 'User';

  return `
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-header">
        <div class="sidebar-logo">T</div>
        <span class="sidebar-brand">TaskFlow</span>
      </div>

      <nav class="sidebar-nav">
        <div class="sidebar-section">
          <div class="sidebar-section-title">Main</div>
          <a class="nav-item" data-route="/dashboard" onclick="window.router.navigate('/dashboard')">
            <span class="nav-icon">📊</span>
            <span class="nav-label">Dashboard</span>
          </a>
          <a class="nav-item" data-route="/board" onclick="window.router.navigate('/board')">
            <span class="nav-icon">📋</span>
            <span class="nav-label">Board</span>
          </a>
          <a class="nav-item" data-route="/tasks" onclick="window.router.navigate('/tasks')">
            <span class="nav-icon">✓</span>
            <span class="nav-label">Tasks</span>
            <span class="nav-badge" id="nav-task-count">0</span>
          </a>
        </div>

        <div class="sidebar-section">
          <div class="sidebar-section-title">Manage</div>
          <a class="nav-item" data-route="/projects" onclick="window.router.navigate('/projects')">
            <span class="nav-icon">📁</span>
            <span class="nav-label">Projects</span>
          </a>
          <a class="nav-item" data-route="/organizations" onclick="window.router.navigate('/organizations')">
            <span class="nav-icon">🏢</span>
            <span class="nav-label">Organizations</span>
          </a>
          <a class="nav-item" data-route="/users" onclick="window.router.navigate('/users')">
            <span class="nav-icon">👥</span>
            <span class="nav-label">Users</span>
          </a>
        </div>

        <div class="sidebar-section">
          <div class="sidebar-section-title">Account</div>
          <a class="nav-item" data-route="/settings" onclick="window.router.navigate('/settings')">
            <span class="nav-icon">⚙</span>
            <span class="nav-label">Settings</span>
          </a>
        </div>
      </nav>

      <div class="sidebar-footer">
        <div class="sidebar-user" onclick="window.router.navigate('/settings')">
          <div class="avatar">${initials.toUpperCase()}</div>
          <div class="sidebar-user-info">
            <div class="sidebar-user-name">${displayName}</div>
            <div class="sidebar-user-role">Member</div>
          </div>
        </div>
      </div>
    </aside>
  `;
}

function updateTaskCount() {
  const el = document.getElementById('nav-task-count');
  if (el) {
    const count = (window.store.get('tasks') || []).length;
    el.textContent = count;
  }
}

window.renderSidebar = renderSidebar;
window.updateTaskCount = updateTaskCount;
