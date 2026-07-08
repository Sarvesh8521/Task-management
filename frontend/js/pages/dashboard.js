/**
 * Dashboard Page
 */
function renderDashboardPage() {
  window.updateHeaderTitle('Dashboard');

  const page = document.getElementById('page-content');
  const tasks = window.store.get('tasks') || [];
  const projects = window.store.get('projects') || [];
  const statusCounts = window.store.getTaskCountByStatus();
  const priorityCounts = window.store.getTaskCountByPriority();
  const total = tasks.length;

  const statusColors = {
    todo: 'var(--color-status-todo)',
    in_progress: 'var(--color-status-in-progress)',
    in_review: 'var(--color-status-in-review)',
    completed: 'var(--color-status-completed)',
    blocked: 'var(--color-status-blocked)',
  };

  const priorityColors = {
    highest: 'var(--color-priority-highest)',
    high: 'var(--color-priority-high)',
    medium: 'var(--color-priority-medium)',
    low: 'var(--color-priority-low)',
    lowest: 'var(--color-priority-lowest)',
  };

  page.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">Dashboard</h1>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="window.showCreateTaskModal()">+ New Task</button>
      </div>
    </div>

    <div class="grid-stats slide-up">
      <div class="stat-card" style="--accent-color:var(--color-primary)">
        <div class="stat-label">Total Tasks</div>
        <div class="stat-value">${total}</div>
        <div class="stat-icon" style="background:var(--color-primary-muted);color:var(--color-primary)">📋</div>
      </div>
      <div class="stat-card" style="--accent-color:var(--color-status-in-progress)">
        <div class="stat-label">In Progress</div>
        <div class="stat-value">${statusCounts.in_progress}</div>
        <div class="stat-icon" style="background:var(--color-info-muted);color:var(--color-info)">🔄</div>
      </div>
      <div class="stat-card" style="--accent-color:var(--color-status-completed)">
        <div class="stat-label">Completed</div>
        <div class="stat-value">${statusCounts.completed}</div>
        <div class="stat-icon" style="background:var(--color-success-muted);color:var(--color-success)">✓</div>
      </div>
      <div class="stat-card" style="--accent-color:var(--color-warning)">
        <div class="stat-label">Projects</div>
        <div class="stat-value">${projects.length}</div>
        <div class="stat-icon" style="background:var(--color-warning-muted);color:var(--color-warning)">📁</div>
      </div>
    </div>

    <div class="dashboard-charts">
      <div class="chart-card slide-up">
        <div class="chart-card-title">Tasks by Status</div>
        <div class="status-bar-chart">
          ${Object.entries(statusCounts).map(([status, count]) => `
            <div class="status-bar-row">
              <span class="status-bar-label">${status.replace('_', ' ')}</span>
              <div class="status-bar-track">
                <div class="status-bar-fill" style="width:${total ? (count/total*100) : 0}%;background:${statusColors[status]}"></div>
              </div>
              <span class="status-bar-count">${count}</span>
            </div>
          `).join('')}
        </div>
      </div>

      <div class="chart-card slide-up">
        <div class="chart-card-title">By Priority</div>
        <div class="priority-list">
          ${Object.entries(priorityCounts).map(([pri, count]) => `
            <div class="priority-item">
              <div style="display:flex;align-items:center;gap:8px">
                <span class="priority-dot" style="background:${priorityColors[pri]}"></span>
                <span style="font-size:13px;text-transform:capitalize">${pri}</span>
              </div>
              <span style="font-weight:600">${count}</span>
            </div>
          `).join('')}
        </div>
      </div>
    </div>

    <div class="chart-card slide-up">
      <div class="chart-card-title">Recent Tasks</div>
      <div class="recent-tasks-list">
        ${tasks.length === 0 ? `
          <div class="empty-state" style="padding:32px">
            <div class="empty-state-icon">📋</div>
            <div class="empty-state-title">No tasks yet</div>
            <div class="empty-state-text">Create your first task to get started</div>
          </div>
        ` : tasks.slice(0, 8).map(task => `
          <div class="recent-task-item" onclick="window.showTaskDetail(${JSON.stringify(task).replace(/"/g, '&quot;')})">
            <span class="badge badge-${task.issue_type}" style="font-size:10px">${window.ISSUE_TYPE_ICONS?.[task.issue_type] || '✅'} ${task.issue_type}</span>
            <span class="recent-task-name truncate">${task.name}</span>
            <span class="badge badge-${task.status}">${task.status.replace('_', ' ')}</span>
            <span class="badge badge-${task.priority}">${task.priority}</span>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

window.renderDashboardPage = renderDashboardPage;
