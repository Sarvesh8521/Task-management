/**
 * Settings Page
 */
window.setTheme = function(theme) {
  if (theme === 'light') {
    document.documentElement.classList.add('theme-light');
    localStorage.setItem('theme', 'light');
    window.toast.success('Light Mode applied');
  } else {
    document.documentElement.classList.remove('theme-light');
    localStorage.setItem('theme', 'dark');
    window.toast.success('Dark Mode applied');
  }
};

function renderSettingsPage() {
  window.updateHeaderTitle('Settings');

  const page = document.getElementById('page-content');
  const user = window.store.get('user') || {};

  page.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">Settings</h1>
    </div>

    <div class="settings-layout slide-up">
      <nav class="settings-nav">
        <a class="nav-item active" data-settings-tab="profile" onclick="switchSettingsTab('profile')">
          <span class="nav-icon">👤</span>
          <span class="nav-label">Profile</span>
        </a>
        <a class="nav-item" data-settings-tab="account" onclick="switchSettingsTab('account')">
          <span class="nav-icon">🔐</span>
          <span class="nav-label">Account</span>
        </a>
        <a class="nav-item" data-settings-tab="appearance" onclick="switchSettingsTab('appearance')">
          <span class="nav-icon">🎨</span>
          <span class="nav-label">Appearance</span>
        </a>
      </nav>

      <div id="settings-panel">
        <div class="settings-section" id="settings-profile">
          <div class="settings-section-title">Profile Information</div>
          <div class="settings-form">
            <div style="display:flex;align-items:center;gap:24px;margin-bottom:16px">
              <div class="avatar avatar-lg" style="width:64px;height:64px;font-size:24px">
                ${(user.first_name?.[0] || 'U').toUpperCase()}${(user.last_name?.[0] || '').toUpperCase()}
              </div>
              <div>
                <div style="font-size:18px;font-weight:600">${user.first_name || ''} ${user.last_name || ''}</div>
                <div style="color:var(--color-text-tertiary);font-size:13px">@${user.username || 'user'}</div>
              </div>
            </div>

            <div class="settings-row">
              <div class="form-group">
                <label class="form-label">First Name</label>
                <input class="form-input" id="settings-first" value="${user.first_name || ''}" />
              </div>
              <div class="form-group">
                <label class="form-label">Last Name</label>
                <input class="form-input" id="settings-last" value="${user.last_name || ''}" />
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Email</label>
              <input class="form-input" type="email" id="settings-email" value="${user.email || ''}" />
            </div>

            <div style="display:flex;justify-content:flex-end">
              <button class="btn btn-primary" onclick="saveProfileSettings()">Save Changes</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}

function switchSettingsTab(tab) {
  document.querySelectorAll('[data-settings-tab]').forEach(el => {
    el.classList.toggle('active', el.dataset.settingsTab === tab);
  });

  const panel = document.getElementById('settings-panel');
  const user = window.store.get('user') || {};

  if (tab === 'profile') {
    renderSettingsPage();
  } else if (tab === 'account') {
    panel.innerHTML = `
      <div class="settings-section">
        <div class="settings-section-title">Account Security</div>
        <div class="settings-form">
          <div class="form-group">
            <label class="form-label">Current Password</label>
            <input class="form-input" type="password" id="settings-current-pw" placeholder="Enter current password" />
          </div>
          <div class="form-group">
            <label class="form-label">New Password</label>
            <input class="form-input" type="password" id="settings-new-pw" placeholder="Enter new password" />
          </div>
          <div class="form-group">
            <label class="form-label">Confirm Password</label>
            <input class="form-input" type="password" id="settings-confirm-pw" placeholder="Confirm new password" />
          </div>
          <div style="display:flex;justify-content:flex-end">
            <button class="btn btn-primary" onclick="window.toast.info('Password change requires backend auth user update')">Update Password</button>
          </div>
        </div>

        <div style="margin-top:32px;padding-top:24px;border-top:1px solid var(--border-color)">
          <div style="font-size:15px;font-weight:600;color:var(--color-danger);margin-bottom:12px">Danger Zone</div>
          <p style="font-size:13px;color:var(--color-text-tertiary);margin-bottom:12px">Once you sign out, you will need to log in again.</p>
          <button class="btn btn-danger" onclick="window.api.clearTokens(); window.dispatchEvent(new CustomEvent('auth:logout'))">Sign Out</button>
        </div>
      </div>
    `;
  } else if (tab === 'appearance') {
    const currentTheme = localStorage.getItem('theme') || 'dark';
    
    panel.innerHTML = `
      <div class="settings-section">
        <div class="settings-section-title">Appearance</div>
        <div class="settings-form">
          <p style="color:var(--color-text-secondary)">TaskFlow uses a dark theme by default for reduced eye strain, but you can switch to a light theme below.</p>
          <div style="display:flex;gap:12px;margin-top:16px">
            <div class="card" onclick="window.setTheme('dark'); switchSettingsTab('appearance')" style="flex:1;cursor:pointer;border-color:var(${currentTheme === 'dark' ? '--color-primary' : '--border-color'});text-align:center;padding:24px;transition:all var(--transition-fast)">
              <div style="font-size:24px;margin-bottom:8px">🌙</div>
              <div style="font-weight:600">Dark Mode</div>
              <div style="font-size:12px;color:var(--color-text-tertiary);margin-top:4px">${currentTheme === 'dark' ? 'Active' : 'Click to select'}</div>
            </div>
            <div class="card" onclick="window.setTheme('light'); switchSettingsTab('appearance')" style="flex:1;cursor:pointer;border-color:var(${currentTheme === 'light' ? '--color-primary' : '--border-color'});text-align:center;padding:24px;transition:all var(--transition-fast)">
              <div style="font-size:24px;margin-bottom:8px">☀️</div>
              <div style="font-weight:600">Light Mode</div>
              <div style="font-size:12px;color:var(--color-text-tertiary);margin-top:4px">${currentTheme === 'light' ? 'Active' : 'Click to select'}</div>
            </div>
          </div>
        </div>
      </div>
    `;
  }
}

function saveProfileSettings() {
  const user = window.store.get('user');
  if (user) {
    user.first_name = document.getElementById('settings-first')?.value || user.first_name;
    user.last_name = document.getElementById('settings-last')?.value || user.last_name;
    user.email = document.getElementById('settings-email')?.value || user.email;
    window.store.set('user', user);
    localStorage.setItem('user', JSON.stringify(user));
    window.toast.success('Profile updated');
  }
}

window.renderSettingsPage = renderSettingsPage;
window.switchSettingsTab = switchSettingsTab;
window.saveProfileSettings = saveProfileSettings;
