/**
 * Simple State Management
 */
class Store {
  constructor() {
    this._state = {
      user: JSON.parse(localStorage.getItem('user') || 'null'),
      tasks: [],
      projects: [],
      organizations: [],
      users: [],
      currentProject: null,
      loading: false,
    };
    this._listeners = new Map();
  }

  get(key) {
    return this._state[key];
  }

  set(key, value) {
    this._state[key] = value;
    this._notify(key, value);
  }

  on(key, callback) {
    if (!this._listeners.has(key)) {
      this._listeners.set(key, new Set());
    }
    this._listeners.get(key).add(callback);
    return () => this._listeners.get(key)?.delete(callback);
  }

  _notify(key, value) {
    const listeners = this._listeners.get(key);
    if (listeners) {
      listeners.forEach(cb => cb(value));
    }
  }

  async loadTasks() {
    try {
      this.set('loading', true);
      const tasks = await window.api.getTasks();
      this.set('tasks', Array.isArray(tasks) ? tasks : []);
    } catch (err) {
      window.toast?.error(err.message);
      this.set('tasks', []);
    } finally {
      this.set('loading', false);
    }
  }

  async loadProjects() {
    try {
      const projects = await window.api.getProjects();
      this.set('projects', Array.isArray(projects) ? projects : []);
    } catch (err) {
      window.toast?.error(err.message);
      this.set('projects', []);
    }
  }

  async loadAll() {
    await Promise.all([this.loadTasks(), this.loadProjects()]);
  }

  getTasksByStatus(statusKey) {
    return this.get('tasks').filter(t => t.status === statusKey);
  }

  getTaskCountByStatus() {
    const tasks = this.get('tasks') || [];
    const counts = { todo: 0, in_progress: 0, in_review: 0, completed: 0, blocked: 0 };
    tasks.forEach(t => { if (counts[t.status] !== undefined) counts[t.status]++; });
    return counts;
  }

  getTaskCountByPriority() {
    const tasks = this.get('tasks') || [];
    const counts = { highest: 0, high: 0, medium: 0, low: 0, lowest: 0 };
    tasks.forEach(t => { if (counts[t.priority] !== undefined) counts[t.priority]++; });
    return counts;
  }
}

window.store = new Store();
