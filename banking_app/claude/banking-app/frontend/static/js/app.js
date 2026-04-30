/* ═══════════════════════════════════════════════════
   SecureBank – Frontend Application
   ═══════════════════════════════════════════════════ */

const API = '/api';
let authToken = localStorage.getItem('sb_token') || null;
let currentUser = JSON.parse(localStorage.getItem('sb_user') || 'null');
let userAccounts = [];

// ── API Helper ──────────────────────────────────────
async function apiFetch(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (authToken) headers['Authorization'] = `Bearer ${authToken}`;

  const res = await fetch(API + path, { ...options, headers });
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const msg = data.detail || 'Ein Fehler ist aufgetreten';
    throw new Error(Array.isArray(msg) ? msg.map(e => e.msg).join(', ') : msg);
  }
  return data;
}

// ── Format Helpers ──────────────────────────────────
function formatMoney(amount) {
  return new Intl.NumberFormat('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amount);
}

function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric' })
    + ' ' + d.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' });
}

function maskIBAN(iban) {
  if (!iban || iban.length < 8) return iban;
  return iban.slice(0, 4) + ' •••• •••• ' + iban.slice(-4);
}

function btnLoading(btn, loading) {
  const span = btn.querySelector('span');
  const loader = btn.querySelector('.btn-loader');
  if (loading) {
    span?.classList.add('hidden');
    loader?.classList.remove('hidden');
    btn.disabled = true;
  } else {
    span?.classList.remove('hidden');
    loader?.classList.add('hidden');
    btn.disabled = false;
  }
}

function showError(id, msg) {
  const el = document.getElementById(id);
  if (el) { el.textContent = msg; }
}
function clearMsg(id) {
  const el = document.getElementById(id);
  if (el) { el.textContent = ''; }
}
function showSuccess(id, msg) {
  const el = document.getElementById(id);
  if (el) { el.textContent = msg; }
}

// ── Auth Tab Toggle ─────────────────────────────────
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const tab = btn.dataset.tab;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(`${tab}-form`).classList.add('active');
    clearMsg('login-error'); clearMsg('reg-error'); clearMsg('reg-success');
  });
});

// ── Login ───────────────────────────────────────────
document.getElementById('login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('.btn-primary');
  clearMsg('login-error');
  btnLoading(btn, true);
  try {
    const data = await apiFetch('/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        email: document.getElementById('login-email').value,
        password: document.getElementById('login-password').value,
      })
    });
    authToken = data.access_token;
    currentUser = data.user;
    localStorage.setItem('sb_token', authToken);
    localStorage.setItem('sb_user', JSON.stringify(currentUser));
    enterDashboard();
  } catch (err) {
    showError('login-error', err.message);
  } finally {
    btnLoading(btn, false);
  }
});

// ── Register ────────────────────────────────────────
document.getElementById('register-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('.btn-primary');
  clearMsg('reg-error'); clearMsg('reg-success');
  btnLoading(btn, true);
  try {
    await apiFetch('/auth/register', {
      method: 'POST',
      body: JSON.stringify({
        full_name: document.getElementById('reg-name').value,
        email: document.getElementById('reg-email').value,
        password: document.getElementById('reg-password').value,
      })
    });
    showSuccess('reg-success', '✓ Konto erstellt! Bitte melden Sie sich an.');
    e.target.reset();
    // Switch to login tab
    document.querySelector('[data-tab="login"]').click();
    document.getElementById('login-email').value = document.getElementById('reg-email')?.value || '';
  } catch (err) {
    showError('reg-error', err.message);
  } finally {
    btnLoading(btn, false);
  }
});

// ── Navigation ──────────────────────────────────────
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const view = link.dataset.view;
    navigateTo(view);
  });
});

document.querySelectorAll('.link-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    navigateTo(btn.dataset.view);
  });
});

function navigateTo(view) {
  document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
  document.querySelector(`[data-view="${view}"]`)?.classList.add('active');
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.getElementById(`view-${view}`)?.classList.add('active');
  loadView(view);
}

async function loadView(view) {
  if (view === 'overview') await loadOverview();
  else if (view === 'transactions') await loadTransactions();
  else if (view === 'transfer') await loadTransferForm();
  else if (view === 'accounts') await loadAccountsList();
}

// ── Dashboard Entry ─────────────────────────────────
async function enterDashboard() {
  document.getElementById('auth-screen').classList.remove('active');
  document.getElementById('dashboard-screen').classList.add('active');

  // Set user info in nav
  const name = currentUser?.full_name || '—';
  document.getElementById('nav-name').textContent = name;
  document.getElementById('nav-email').textContent = currentUser?.email || '';
  document.getElementById('nav-avatar').textContent = name.charAt(0).toUpperCase();
  document.getElementById('greeting-name').textContent = name.split(' ')[0];

  await loadOverview();
}

// ── Overview ────────────────────────────────────────
async function loadOverview() {
  await loadAccounts();
  const total = userAccounts.reduce((s, a) => s + a.balance, 0);
  document.getElementById('total-balance').textContent = `€ ${formatMoney(total)}`;

  // Render account cards
  const grid = document.getElementById('overview-accounts');
  grid.innerHTML = userAccounts.map(acc => `
    <div class="account-card">
      <div class="account-card-type">${acc.account_type}</div>
      <div class="account-card-number">${maskIBAN(acc.account_number)}</div>
      <div class="account-card-balance">€ ${formatMoney(acc.balance)}<span class="account-card-currency">${acc.currency}</span></div>
    </div>
  `).join('');

  // Recent transactions
  const txs = await apiFetch('/transactions?limit=6').catch(() => []);
  renderTransactionsList('recent-transactions', txs);
}

// ── Accounts ────────────────────────────────────────
async function loadAccounts() {
  userAccounts = await apiFetch('/accounts').catch(() => []);
  return userAccounts;
}

async function loadAccountsList() {
  await loadAccounts();
  const list = document.getElementById('accounts-list');
  list.innerHTML = userAccounts.map(acc => `
    <div class="account-list-item">
      <div class="ali-info">
        <div class="ali-type">${acc.account_type}</div>
        <div class="ali-number">${acc.account_number}</div>
      </div>
      <div class="ali-balance">€ ${formatMoney(acc.balance)}</div>
    </div>
  `).join('') || '<p style="color:var(--text3);padding:20px">Keine Konten vorhanden.</p>';
}

// New account modal
document.getElementById('new-account-btn')?.addEventListener('click', () => {
  document.getElementById('new-account-modal').classList.remove('hidden');
});
document.getElementById('modal-cancel')?.addEventListener('click', () => {
  document.getElementById('new-account-modal').classList.add('hidden');
});
document.getElementById('modal-confirm')?.addEventListener('click', async () => {
  clearMsg('new-account-error');
  const type = document.getElementById('new-account-type').value;
  try {
    await apiFetch('/accounts', {
      method: 'POST',
      body: JSON.stringify({ account_type: type })
    });
    document.getElementById('new-account-modal').classList.add('hidden');
    await loadAccountsList();
  } catch (err) {
    showError('new-account-error', err.message);
  }
});

// ── Transactions ────────────────────────────────────
async function loadTransactions() {
  await loadAccounts();
  const filter = document.getElementById('tx-account-filter');
  filter.innerHTML = '<option value="">Alle Konten</option>' +
    userAccounts.map(a => `<option value="${a.id}">${a.account_type} – ${a.account_number.slice(-6)}</option>`).join('');

  const selectedId = filter.value;
  const url = selectedId ? `/transactions?account_id=${selectedId}&limit=100` : '/transactions?limit=100';
  const txs = await apiFetch(url).catch(() => []);
  renderTransactionsList('all-transactions', txs);
}

document.getElementById('tx-account-filter')?.addEventListener('change', loadTransactions);

function renderTransactionsList(containerId, txs) {
  const container = document.getElementById(containerId);
  if (!txs.length) {
    container.innerHTML = '<div class="tx-empty">Keine Transaktionen vorhanden</div>';
    return;
  }

  const accountIdSet = new Set(userAccounts.map(a => a.id));

  container.innerHTML = txs.map(tx => {
    const isOut = accountIdSet.has(tx.from_account_id);
    const sign = isOut ? '−' : '+';
    const cls = isOut ? 'out' : 'in';
    const icon = isOut ? '↑' : '↓';
    const desc = tx.description || tx.transaction_type;
    return `
      <div class="tx-item">
        <div class="tx-icon ${cls}">${icon}</div>
        <div class="tx-info">
          <div class="tx-desc">${escapeHtml(desc)}</div>
          <div class="tx-ref">${tx.reference}</div>
        </div>
        <div class="tx-date">${formatDate(tx.created_at)}</div>
        <div class="tx-amount ${cls}">${sign} € ${formatMoney(tx.amount)}</div>
      </div>
    `;
  }).join('');
}

// ── Transfer Form ───────────────────────────────────
async function loadTransferForm() {
  await loadAccounts();
  const sel = document.getElementById('transfer-from');
  sel.innerHTML = userAccounts.map(a =>
    `<option value="${a.id}">${a.account_type} – ${maskIBAN(a.account_number)} (€ ${formatMoney(a.balance)})</option>`
  ).join('');
}

document.getElementById('transfer-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('.btn-primary');
  clearMsg('transfer-error'); clearMsg('transfer-success');
  btnLoading(btn, true);
  try {
    const tx = await apiFetch('/transactions/transfer', {
      method: 'POST',
      body: JSON.stringify({
        from_account_id: parseInt(document.getElementById('transfer-from').value),
        to_account_number: document.getElementById('transfer-to').value.trim(),
        amount: parseFloat(document.getElementById('transfer-amount').value),
        description: document.getElementById('transfer-desc').value.trim(),
      })
    });
    showSuccess('transfer-success', `✓ Überweisung erfolgreich! Referenz: ${tx.reference}`);
    e.target.querySelector('#transfer-to').value = '';
    e.target.querySelector('#transfer-amount').value = '';
    e.target.querySelector('#transfer-desc').value = '';
    await loadTransferForm(); // refresh balances
  } catch (err) {
    showError('transfer-error', err.message);
  } finally {
    btnLoading(btn, false);
  }
});

// ── Logout ──────────────────────────────────────────
document.getElementById('logout-btn')?.addEventListener('click', () => {
  authToken = null;
  currentUser = null;
  userAccounts = [];
  localStorage.removeItem('sb_token');
  localStorage.removeItem('sb_user');
  document.getElementById('dashboard-screen').classList.remove('active');
  document.getElementById('auth-screen').classList.add('active');
});

// ── Escape HTML ─────────────────────────────────────
function escapeHtml(str) {
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ── Auto-login on page load ─────────────────────────
(async () => {
  if (authToken && currentUser) {
    try {
      // Verify token is still valid
      await apiFetch('/auth/me');
      await enterDashboard();
    } catch {
      localStorage.removeItem('sb_token');
      localStorage.removeItem('sb_user');
      authToken = null; currentUser = null;
    }
  }
})();
