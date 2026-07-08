/**
 * Login Page
 */
function renderLoginPage() {
  const app = document.getElementById('app');
  app.innerHTML = `
    <div class="login-page">
      <div class="login-card fade-in">
        <div class="login-logo">
          <div class="login-logo-icon">T</div>
          <span class="login-logo-text">TaskFlow</span>
        </div>

        <div id="login-error" style="display:none" class="login-error"></div>

        <form class="login-form" id="login-form">
          <div class="form-group">
            <label class="form-label" for="login-username">Username</label>
            <input class="form-input" type="text" id="login-username"
                   placeholder="Enter your username" autocomplete="username" required />
          </div>

          <div class="form-group">
            <label class="form-label" for="login-password">Password</label>
            <input class="form-input" type="password" id="login-password"
                   placeholder="Enter your password" autocomplete="current-password" required />
          </div>

          <button class="btn btn-primary" type="submit" id="login-submit">
            <span id="login-btn-text">Sign In</span>
            <div class="spinner" id="login-spinner" style="display:none"></div>
          </button>
        </form>

        <p style="text-align:center;margin-top:24px;font-size:14px;color:var(--color-text-secondary);">
          Don't have an account? <a href="#" onclick="event.preventDefault(); window.renderRegisterPage()" style="color:var(--color-primary);text-decoration:none;font-weight:500">Sign Up</a>
        </p>

        <p style="text-align:center;margin-top:16px;font-size:12px;color:var(--color-text-tertiary);">
          Task Management System • Built with Django & Vanilla JS
        </p>
      </div>
    </div>
  `;

  document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;
    const errorEl = document.getElementById('login-error');
    const btnText = document.getElementById('login-btn-text');
    const spinner = document.getElementById('login-spinner');
    const submitBtn = document.getElementById('login-submit');

    errorEl.style.display = 'none';
    btnText.textContent = 'Signing in...';
    spinner.style.display = 'inline-block';
    submitBtn.disabled = true;

    try {
      const data = await window.api.login(username, password);
      window.store.set('user', data.user);
      window.toast.success(`Welcome back, ${data.user.first_name || data.user.username}!`);
      initApp();
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.style.display = 'block';
      btnText.textContent = 'Sign In';
      spinner.style.display = 'none';
      submitBtn.disabled = false;
    }
  });
}

window.renderLoginPage = renderLoginPage;
