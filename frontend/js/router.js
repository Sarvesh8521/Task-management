/**
 * Client-side SPA Router
 */
class Router {
  constructor() {
    this._routes = new Map();
    this._currentRoute = null;
    window.addEventListener('popstate', () => this._handleRoute());
  }

  register(path, handler) {
    this._routes.set(path, handler);
  }

  navigate(path) {
    if (path === this._currentRoute) return;
    window.history.pushState({}, '', `#${path}`);
    this._handleRoute();
  }

  _handleRoute() {
    const hash = window.location.hash.slice(1) || '/dashboard';
    this._currentRoute = hash;

    // Update active nav item
    document.querySelectorAll('.nav-item').forEach(el => {
      el.classList.toggle('active', el.dataset.route === hash);
    });

    const handler = this._routes.get(hash);
    if (handler) {
      handler();
    } else {
      // Try to find a matching route
      const defaultHandler = this._routes.get('/dashboard');
      if (defaultHandler) defaultHandler();
    }
  }

  start() {
    this._handleRoute();
  }

  get current() {
    return this._currentRoute;
  }
}

window.router = new Router();
