/**
 * Kanban Board Page
 */
const BOARD_COLUMNS = [
  { key: 'todo', label: 'To Do', color: 'var(--color-status-todo)' },
  { key: 'in_progress', label: 'In Progress', color: 'var(--color-status-in-progress)' },
  { key: 'in_review', label: 'In Review', color: 'var(--color-status-in-review)' },
  { key: 'completed', label: 'Completed', color: 'var(--color-status-completed)' },
  { key: 'blocked', label: 'Blocked', color: 'var(--color-status-blocked)' },
];

function renderBoardPage() {
  window.updateHeaderTitle('Board');

  const page = document.getElementById('page-content');
  const tasks = window.store.get('tasks') || [];

  page.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">Kanban Board</h1>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="window.showCreateTaskModal()">+ New Task</button>
      </div>
    </div>

    <div class="board-container" id="board-container">
      ${BOARD_COLUMNS.map(col => {
        const colTasks = tasks.filter(t => t.status === col.key);
        return `
          <div class="board-column slide-up">
            <div class="board-column-header">
              <div class="board-column-title">
                <span class="board-column-dot" style="background:${col.color}"></span>
                ${col.label}
              </div>
              <span class="board-column-count">${colTasks.length}</span>
            </div>
            <div class="board-column-cards" data-status="${col.key}"
                 ondragover="handleColumnDragOver(event)"
                 ondragleave="handleColumnDragLeave(event)"
                 ondrop="handleColumnDrop(event)">
              ${colTasks.length === 0 ? `
                <div style="padding:24px 12px;text-align:center;color:var(--color-text-tertiary);font-size:13px;">
                  No tasks
                </div>
              ` : colTasks.map(task => window.renderTaskCard(task)).join('')}
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;

  // Add click handlers to task cards
  page.querySelectorAll('.task-card').forEach(card => {
    card.addEventListener('click', (e) => {
      if (e.target.closest('[draggable]') && e.detail === 1) {
        const taskId = parseInt(card.dataset.taskId);
        const task = tasks.find(t => t.id === taskId);
        if (task) window.showTaskDetail(task);
      }
    });
  });
}

function handleColumnDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  e.currentTarget.classList.add('drag-over');
}

function handleColumnDragLeave(e) {
  e.currentTarget.classList.remove('drag-over');
}

async function handleColumnDrop(e) {
  e.preventDefault();
  e.currentTarget.classList.remove('drag-over');

  const taskId = parseInt(e.dataTransfer.getData('text/plain'));
  const newStatus = e.currentTarget.dataset.status;

  if (!taskId || !newStatus) return;

  const task = (window.store.get('tasks') || []).find(t => t.id === taskId);
  if (!task || task.status === newStatus) return;

  try {
    await window.api.updateTask(taskId, { ...task, status: newStatus });
    window.toast.success(`Task moved to ${newStatus.replace('_', ' ')}`);
    await window.store.loadTasks();
    renderBoardPage();
  } catch (err) {
    window.toast.error(err.message);
  }
}

window.renderBoardPage = renderBoardPage;
window.handleColumnDragOver = handleColumnDragOver;
window.handleColumnDragLeave = handleColumnDragLeave;
window.handleColumnDrop = handleColumnDrop;
