/**
 * API Client — Centralized fetch wrapper with JWT authentication.
 */
const API_BASE = '/api';

class ApiClient {
  constructor() {
    this._accessToken = localStorage.getItem('access_token');
    this._refreshToken = localStorage.getItem('refresh_token');
  }

  get isAuthenticated() {
    return !!this._accessToken;
  }

  setTokens(access, refresh) {
    this._accessToken = access;
    this._refreshToken = refresh;
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  }

  clearTokens() {
    this._accessToken = null;
    this._refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }

  async _fetch(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const headers = { 'Content-Type': 'application/json', ...options.headers };

    if (this._accessToken) {
      headers['Authorization'] = `Bearer ${this._accessToken}`;
    }

    try {
      let response = await fetch(url, { ...options, headers });

      // If 401 and we have a refresh token, try to refresh
      if (response.status === 401 && this._refreshToken) {
        const refreshed = await this._refreshAccessToken();
        if (refreshed) {
          headers['Authorization'] = `Bearer ${this._accessToken}`;
          response = await fetch(url, { ...options, headers });
        } else {
          this.clearTokens();
          window.dispatchEvent(new CustomEvent('auth:logout'));
          throw new Error('Session expired. Please log in again.');
        }
      }

      const data = await response.json();

      if (!response.ok) {
        const errorMsg = data.error || data.detail || JSON.stringify(data);
        throw new Error(errorMsg);
      }

      return data;
    } catch (err) {
      if (err.name === 'TypeError' && err.message === 'Failed to fetch') {
        throw new Error('Unable to connect to server. Please check your connection.');
      }
      throw err;
    }
  }

  async _refreshAccessToken() {
    try {
      const response = await fetch(`${API_BASE}/auth/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: this._refreshToken }),
      });

      if (!response.ok) return false;

      const data = await response.json();
      this._accessToken = data.access;
      localStorage.setItem('access_token', data.access);
      if (data.refresh) {
        this._refreshToken = data.refresh;
        localStorage.setItem('refresh_token', data.refresh);
      }
      return true;
    } catch {
      return false;
    }
  }

  // Auth
  async login(username, password) {
    const data = await this._fetch('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    this.setTokens(data.access, data.refresh);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  }

  // Users
  getUser(id) { return this._fetch(`/users/${id}/`); }
  createUser(data) { return this._fetch('/users/create/', { method: 'POST', body: JSON.stringify(data) }); }
  updateUser(id, data) { return this._fetch(`/users/update/${id}/`, { method: 'PUT', body: JSON.stringify(data) }); }
  deleteUser(id) { return this._fetch(`/users/delete/${id}/`, { method: 'DELETE' }); }
  searchUsers(params) { return this._fetch(`/users/search/?${new URLSearchParams(params)}`); }

  // Tasks
  getTasks() { return this._fetch('/tasks/all/'); }
  createTask(data) { return this._fetch('/tasks/create/', { method: 'POST', body: JSON.stringify(data) }); }
  updateTask(id, data) { return this._fetch(`/tasks/update/${id}/`, { method: 'PUT', body: JSON.stringify(data) }); }
  assignTask(taskId, userId) { return this._fetch(`/tasks/assign/${taskId}/${userId}/`, { method: 'POST' }); }
  searchTasks(query) { return this._fetch(`/tasks/search/?query=${encodeURIComponent(query)}`); }
  deleteTask(id) { return this._fetch(`/tasks/delete/${id}/`, { method: 'DELETE' }); }

  // Projects
  getProjects() { return this._fetch('/projects/all/'); }
  createProject(data) { return this._fetch('/projects/create/', { method: 'POST', body: JSON.stringify(data) }); }
  updateProject(id, data) { return this._fetch(`/projects/update/${id}/`, { method: 'PUT', body: JSON.stringify(data) }); }
  deleteProject(id) { return this._fetch(`/projects/delete/${id}/`, { method: 'DELETE' }); }

  // Organizations
  getOrganization(id) { return this._fetch(`/organizations/${id}/`); }
  createOrganization(data) { return this._fetch('/organizations/create/', { method: 'POST', body: JSON.stringify(data) }); }
  updateOrganization(id, data) { return this._fetch(`/organizations/update/${id}/`, { method: 'PUT', body: JSON.stringify(data) }); }
  deleteOrganization(id) { return this._fetch(`/organizations/delete/${id}/`, { method: 'DELETE' }); }

  // Profiles
  getProfile(userId) { return this._fetch(`/profiles/${userId}/`); }
  createProfile(data) { return this._fetch('/profiles/create/', { method: 'POST', body: JSON.stringify(data) }); }
  updateProfile(userId, data) { return this._fetch(`/profiles/update/${userId}/`, { method: 'PUT', body: JSON.stringify(data) }); }
}

window.api = new ApiClient();
