/**
 * Header Component
 */
function renderHeader(title = 'Dashboard') {
  return `
    <header class="header">
      <div class="header-left">
        <div class="header-breadcrumb">
          <span>TaskFlow</span>
          <span>›</span>
          <span class="current" id="header-title">${title}</span>
        </div>
      </div>
      <div class="header-right">
        <div class="header-search" id="header-search">
          <span class="header-search-icon">🔍</span>
          <input type="text" placeholder="Search tasks..." id="header-search-input" />
        </div>
        <button class="btn btn-ghost btn-icon" data-tooltip="Notifications" id="btn-notifications">🔔</button>
        <button class="btn btn-ghost btn-icon" data-tooltip="Logout" id="btn-logout">⏻</button>
      </div>
    </header>
  `;
}

function initHeaderEvents() {
  const searchInput = document.getElementById('header-search-input');
  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(async () => {
        const query = e.target.value.trim();
        if (query.length >= 2) {
          try {
            const results = await window.api.searchTasks(query);
            window.store.set('searchResults', Array.isArray(results) ? results : []);
            showSearchResults(results);
          } catch (err) {
            console.error('Search failed:', err);
          }
        }
      }, 300);
    });
  }

  const logoutBtn = document.getElementById('btn-logout');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      window.api.clearTokens();
      window.store.set('user', null);
      window.store.set('tasks', []);
      window.store.set('projects', []);
      window.dispatchEvent(new CustomEvent('auth:logout'));
    });
  }
}

function showSearchResults(results) {
  // Remove existing dropdown
  const existing = document.getElementById('search-results-dropdown');
  if (existing) existing.remove();

  if (!results || results.length === 0) return;

  const dropdown = document.createElement('div');
  dropdown.className = 'dropdown-menu';
  dropdown.id = 'search-results-dropdown';
  dropdown.style.cssText = 'position:absolute;top:100%;left:0;right:0;margin-top:4px;max-height:300px;overflow-y:auto;';

  results.slice(0, 8).forEach(task => {
    const item = document.createElement('button');
    item.className = 'dropdown-item';
    item.innerHTML = `
      <span class="badge badge-${task.issue_type}" style="font-size:10px">${task.issue_type}</span>
      <span class="truncate">${task.name}</span>
    `;
    item.addEventListener('click', () => {
      dropdown.remove();
      window.showTaskDetail(task);
    });
    dropdown.appendChild(item);
  });

  const searchEl = document.getElementById('header-search');
  searchEl.style.position = 'relative';
  searchEl.appendChild(dropdown);

  // Close on outside click
  setTimeout(() => {
    document.addEventListener('click', function handler(e) {
      if (!searchEl.contains(e.target)) {
        dropdown.remove();
        document.removeEventListener('click', handler);
      }
    });
  }, 10);
}

function updateHeaderTitle(title) {
  const el = document.getElementById('header-title');
  if (el) el.textContent = title;
}

window.renderHeader = renderHeader;
window.initHeaderEvents = initHeaderEvents;
window.updateHeaderTitle = updateHeaderTitle;
