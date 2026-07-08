/**
 * Tasks List Page
 */
function renderTasksPage() {
  window.updateHeaderTitle('Tasks');

  const page = document.getElementById('page-content');
  const tasks = window.store.get('tasks') || [];

  page.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">All Tasks</h1>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="window.showCreateTaskModal()">+ New Task</button>
      </div>
    </div>

    <div class="task-list-toolbar">
      <div class="filter-group">
        <select class="form-select" id="filter-status" onchange="filterTasks()">
          <option value="">All Status</option>
          <option value="todo">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="in_review">In Review</option>
          <option value="completed">Completed</option>
          <option value="blocked">Blocked</option>
        </select>
      </div>
      <div class="filter-group">
        <select class="form-select" id="filter-priority" onchange="filterTasks()">
          <option value="">All Priority</option>
          <option value="highest">Highest</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
          <option value="lowest">Lowest</option>
        </select>
      </div>
      <div class="filter-group">
        <select class="form-select" id="filter-type" onchange="filterTasks()">
          <option value="">All Types</option>
          <option value="epic">Epic</option>
          <option value="story">Story</option>
          <option value="task">Task</option>
          <option value="bug">Bug</option>
          <option value="subtask">Sub-task</option>
        </select>
      </div>
      <span style="color:var(--color-text-tertiary);font-size:13px" id="tasks-count">${tasks.length} tasks</span>
    </div>

    <div class="table-container slide-up">
      <table class="data-table" id="tasks-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Type</th>
            <th>Name</th>
            <th>Status</th>
            <th>Priority</th>
            <th>Sprint</th>
            <th>Assigned</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody id="tasks-tbody">
          ${renderTaskRows(tasks)}
        </tbody>
      </table>
    </div>
  `;
}

function renderTaskRows(tasks) {
  if (tasks.length === 0) {
    return `<tr><td colspan="8">
      <div class="empty-state" style="padding:32px">
        <div class="empty-state-icon">📋</div>
        <div class="empty-state-title">No tasks found</div>
      </div>
    </td></tr>`;
  }

  return tasks.map(task => `
    <tr style="cursor:pointer" onclick='window.showTaskDetail(${JSON.stringify(task).replace(/'/g, "&#39;")})'>
      <td style="color:var(--color-text-tertiary)">#${task.id}</td>
      <td><span class="badge badge-${task.issue_type}">${window.ISSUE_TYPE_ICONS?.[task.issue_type] || '✅'} ${task.issue_type}</span></td>
      <td style="font-weight:500;max-width:300px" class="truncate">${task.name}</td>
      <td><span class="badge badge-${task.status}">${task.status.replace('_', ' ')}</span></td>
      <td><span class="badge badge-${task.priority}">${task.priority}</span></td>
      <td style="color:var(--color-text-secondary)">${task.sprint || '-'}</td>
      <td><div class="avatar avatar-sm">${task.users}</div></td>
      <td>
        <button class="btn btn-ghost btn-sm" onclick="event.stopPropagation(); deleteTaskRow(${task.id})" title="Delete">🗑</button>
      </td>
    </tr>
  `).join('');
}

function filterTasks() {
  const status = document.getElementById('filter-status').value;
  const priority = document.getElementById('filter-priority').value;
  const type = document.getElementById('filter-type').value;

  let tasks = window.store.get('tasks') || [];
  if (status) tasks = tasks.filter(t => t.status === status);
  if (priority) tasks = tasks.filter(t => t.priority === priority);
  if (type) tasks = tasks.filter(t => t.issue_type === type);

  document.getElementById('tasks-tbody').innerHTML = renderTaskRows(tasks);
  document.getElementById('tasks-count').textContent = `${tasks.length} tasks`;
}

async function deleteTaskRow(taskId) {
  const confirmed = await Modal.confirm('Are you sure you want to delete this task?');
  if (confirmed) {
    try {
      await window.api.deleteTask(taskId);
      window.toast.success('Task deleted');
      await window.store.loadTasks();
      renderTasksPage();
    } catch (err) {
      window.toast.error(err.message);
    }
  }
}

window.renderTasksPage = renderTasksPage;
window.filterTasks = filterTasks;
window.deleteTaskRow = deleteTaskRow;
