/**
 * Task Card Component (used in Kanban Board)
 */
const ISSUE_TYPE_ICONS = {
  epic: '⚡', story: '📖', task: '✅', bug: '🐛', subtask: '🔹',
};

const PRIORITY_ICONS = {
  highest: '🔴', high: '🟠', medium: '🟡', low: '🟢', lowest: '⚪',
};

function renderTaskCard(task) {
  const typeIcon = ISSUE_TYPE_ICONS[task.issue_type] || '✅';
  const priorityIcon = PRIORITY_ICONS[task.priority] || '🟡';

  return `
    <div class="task-card" draggable="true" data-task-id="${task.id}"
         ondragstart="handleDragStart(event)" ondragend="handleDragEnd(event)">
      <div class="task-card-type">
        <span class="task-card-type-icon">${typeIcon}</span>
        <span class="badge badge-${task.issue_type}">${task.issue_type}</span>
        <span class="task-card-id">#${task.id}</span>
      </div>
      <div class="task-card-name" title="${task.name}">${task.name}</div>
      <div class="task-card-footer">
        <div class="task-card-meta">
          <span class="badge badge-${task.priority}" title="Priority: ${task.priority}">${priorityIcon} ${task.priority}</span>
        </div>
        <div class="avatar avatar-sm" title="User #${task.users}">${task.users}</div>
      </div>
    </div>
  `;
}

// Task Detail Modal
function showTaskDetail(task) {
  const projects = window.store.get('projects') || [];
  const project = projects.find(p => p.id === task.project);

  const body = document.createElement('div');
  body.innerHTML = `
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">
      <span class="badge badge-${task.issue_type}">${ISSUE_TYPE_ICONS[task.issue_type] || ''} ${task.issue_type}</span>
      <span class="badge badge-${task.status}">${task.status.replace('_', ' ')}</span>
      <span class="badge badge-${task.priority}">${PRIORITY_ICONS[task.priority] || ''} ${task.priority}</span>
    </div>

    <div class="form-group">
      <label class="form-label">Name</label>
      <input class="form-input" id="detail-name" value="${task.name}" />
    </div>

    <div class="form-group">
      <label class="form-label">Description</label>
      <textarea class="form-textarea" id="detail-desc">${task.description || ''}</textarea>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
      <div class="form-group">
        <label class="form-label">Status</label>
        <select class="form-select" id="detail-status">
          ${['todo','in_progress','in_review','completed','blocked'].map(s =>
            `<option value="${s}" ${s === task.status ? 'selected' : ''}>${s.replace('_', ' ')}</option>`
          ).join('')}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Priority</label>
        <select class="form-select" id="detail-priority">
          ${['highest','high','medium','low','lowest'].map(p =>
            `<option value="${p}" ${p === task.priority ? 'selected' : ''}>${p}</option>`
          ).join('')}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Issue Type</label>
        <select class="form-select" id="detail-type">
          ${['epic','story','task','bug','subtask'].map(t =>
            `<option value="${t}" ${t === task.issue_type ? 'selected' : ''}>${t}</option>`
          ).join('')}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Sprint</label>
        <input class="form-input" id="detail-sprint" value="${task.sprint || ''}" />
      </div>
      <div class="form-group">
        <label class="form-label">Start Date</label>
        <input class="form-input" type="date" id="detail-start" value="${task.start_date || ''}" />
      </div>
      <div class="form-group">
        <label class="form-label">End Date</label>
        <input class="form-input" type="date" id="detail-end" value="${task.end_date || ''}" />
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">Project</label>
      <select class="form-select" id="detail-project">
        ${projects.map(p => `<option value="${p.id}" ${p.id === task.project ? 'selected' : ''}>${p.name}</option>`).join('')}
      </select>
    </div>
  `;

  const footer = document.createElement('div');
  footer.style.cssText = 'display:flex;gap:12px;justify-content:space-between;width:100%';
  footer.innerHTML = `
    <button class="btn btn-danger btn-sm" id="detail-delete">Delete</button>
    <div style="display:flex;gap:12px">
      <button class="btn btn-secondary" id="detail-cancel">Cancel</button>
      <button class="btn btn-primary" id="detail-save">Save Changes</button>
    </div>
  `;

  Modal.open({ title: `Task #${task.id}`, body, footer, wide: true });

  footer.querySelector('#detail-cancel').addEventListener('click', () => Modal.close());

  footer.querySelector('#detail-save').addEventListener('click', async () => {
    try {
      await window.api.updateTask(task.id, {
        name: document.getElementById('detail-name').value,
        description: document.getElementById('detail-desc').value,
        status: document.getElementById('detail-status').value,
        priority: document.getElementById('detail-priority').value,
        issue_type: document.getElementById('detail-type').value,
        sprint: document.getElementById('detail-sprint').value,
        start_date: document.getElementById('detail-start').value || null,
        end_date: document.getElementById('detail-end').value || null,
        project: parseInt(document.getElementById('detail-project').value),
        users: task.users,
      });
      Modal.close();
      window.toast.success('Task updated successfully');
      await window.store.loadTasks();
      // Re-render current page
      const route = window.router.current;
      if (route) window.router.navigate(route);
    } catch (err) {
      window.toast.error(err.message);
    }
  });

  footer.querySelector('#detail-delete').addEventListener('click', async () => {
    const confirmed = await Modal.confirm('Are you sure you want to delete this task?');
    if (confirmed) {
      try {
        await window.api.deleteTask(task.id);
        window.toast.success('Task deleted');
        await window.store.loadTasks();
        const route = window.router.current;
        if (route) window.router.navigate(route);
      } catch (err) {
        window.toast.error(err.message);
      }
    }
  });

  // Make card clickable
  body.querySelectorAll('.task-card').forEach(card => {
    card.addEventListener('click', () => {
      const taskId = parseInt(card.dataset.taskId);
      const clickedTask = window.store.get('tasks').find(t => t.id === taskId);
      if (clickedTask) showTaskDetail(clickedTask);
    });
  });
}

// Drag and Drop handlers
function handleDragStart(e) {
  e.target.classList.add('dragging');
  e.dataTransfer.setData('text/plain', e.target.dataset.taskId);
  e.dataTransfer.effectAllowed = 'move';
}

function handleDragEnd(e) {
  e.target.classList.remove('dragging');
  document.querySelectorAll('.board-column-cards').forEach(col => col.classList.remove('drag-over'));
}

window.renderTaskCard = renderTaskCard;
window.showTaskDetail = showTaskDetail;
window.handleDragStart = handleDragStart;
window.handleDragEnd = handleDragEnd;
window.ISSUE_TYPE_ICONS = ISSUE_TYPE_ICONS;
window.PRIORITY_ICONS = PRIORITY_ICONS;
