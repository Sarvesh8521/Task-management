/**
 * Register Page
 */
function renderRegisterPage() {
  const app = document.getElementById('app');
  app.innerHTML = `
    <div class="login-page">
      <div class="login-card fade-in">
        <div class="login-logo">
          <div class="login-logo-icon">T</div>
          <span class="login-logo-text">TaskFlow</span>
        </div>

        <h2 style="text-align:center;margin-bottom:24px;font-size:20px;font-weight:600">Create an Account</h2>

        <div id="register-error" style="display:none" class="login-error"></div>

        <form class="login-form" id="register-form">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div class="form-group">
              <label class="form-label" for="reg-first">First Name</label>
              <input class="form-input" type="text" id="reg-first" placeholder="Jane" required />
            </div>
            <div class="form-group">
              <label class="form-label" for="reg-last">Last Name</label>
              <input class="form-input" type="text" id="reg-last" placeholder="Doe" required />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" for="reg-username">Username</label>
            <input class="form-input" type="text" id="reg-username" placeholder="Choose a username" required />
          </div>

          <div class="form-group">
            <label class="form-label" for="reg-email">Email</label>
            <input class="form-input" type="email" id="reg-email" placeholder="jane@example.com" required />
          </div>

          <div class="form-group">
            <label class="form-label" for="reg-password">Password</label>
            <input class="form-input" type="password" id="reg-password" placeholder="Min 8 chars, 1 uppercase, 1 special char" required />
          </div>

          <button class="btn btn-primary" type="submit" id="register-submit" style="margin-top:8px">
            <span id="register-btn-text">Sign Up</span>
            <div class="spinner" id="register-spinner" style="display:none"></div>
          </button>
        </form>

        <p style="text-align:center;margin-top:24px;font-size:14px;color:var(--color-text-secondary);">
          Already have an account? <a href="#" onclick="event.preventDefault(); window.renderLoginPage()" style="color:var(--color-primary);text-decoration:none;font-weight:500">Sign In</a>
        </p>
      </div>
    </div>
  `;

  document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorEl = document.getElementById('register-error');
    const btnText = document.getElementById('register-btn-text');
    const spinner = document.getElementById('register-spinner');
    const submitBtn = document.getElementById('register-submit');

    const data = {
      user_name: document.getElementById('reg-username').value.trim(),
      email_id: document.getElementById('reg-email').value.trim(),
      password: document.getElementById('reg-password').value,
      first_name: document.getElementById('reg-first').value.trim(),
      last_name: document.getElementById('reg-last').value.trim(),
    };

    errorEl.style.display = 'none';
    btnText.textContent = 'Creating account...';
    spinner.style.display = 'inline-block';
    submitBtn.disabled = true;

    try {
      // Create user via open endpoint
      await window.api.createUser(data);
      window.toast.success('Account created successfully! Please log in.');
      // Auto redirect to login
      window.renderLoginPage();
    } catch (err) {
      errorEl.textContent = err.message || 'Registration failed';
      errorEl.style.display = 'block';
      btnText.textContent = 'Sign Up';
      spinner.style.display = 'none';
      submitBtn.disabled = false;
    }
  });
}

window.renderRegisterPage = renderRegisterPage;
