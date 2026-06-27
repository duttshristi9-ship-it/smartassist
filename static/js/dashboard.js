// SmartAssist Dashboard + Global JS
document.addEventListener('DOMContentLoaded', function() {
    initSidebar();
    initAlerts();
    animateCounters();
});

function initSidebar() {
    const toggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            if (overlay) overlay.classList.toggle('active');
        });
    }
    if (overlay) {
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        });
    }
}

function initAlerts() {
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => alert.style.opacity = '0', 4000);
        setTimeout(() => alert.remove(), 4500);
    });
}

function animateCounters() {
    document.querySelectorAll('[data-count]').forEach(el => {
        const target = parseInt(el.dataset.count);
        if (isNaN(target)) return;
        let current = 0;
        const step = Math.max(1, Math.ceil(target / 40));
        const timer = setInterval(() => {
            current = Math.min(current + step, target);
            el.textContent = current.toLocaleString();
            if (current >= target) clearInterval(timer);
        }, 30);
    });
}

// Admin: Toggle user status
function toggleUser(userId) {
    fetch(`/admin/users/${userId}/toggle`, {method:'POST', headers:{'Content-Type':'application/json'}})
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                const btn = document.getElementById(`toggle-${userId}`);
                const badge = document.getElementById(`status-${userId}`);
                if (btn) btn.textContent = data.is_active ? '🚫 Deactivate' : '✅ Activate';
                if (badge) {
                    badge.textContent = data.is_active ? 'Active' : 'Inactive';
                    badge.className = `badge ${data.is_active ? 'badge-success' : 'badge-danger'}`;
                }
            }
        });
}

// Admin: Update report status
function updateStatus(reportId, status) {
    fetch(`/admin/reports/${reportId}/status`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({status})
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            const el = document.getElementById(`status-${reportId}`);
            const labels = {open:'Open',in_progress:'In Progress',resolved:'Resolved',closed:'Closed'};
            const classes = {open:'badge-danger',in_progress:'badge-warning',resolved:'badge-success',closed:'badge-secondary'};
            if (el) { el.textContent = labels[status]; el.className = `badge ${classes[status]}`; }
            showToast(`Report #${reportId} updated to ${labels[status]}`, 'success');
        }
    });
}

// Toast notification
function showToast(message, type='info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type}`;
    toast.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;min-width:280px;animation:fadeInUp .3s ease';
    toast.innerHTML = `<span>${type === 'success' ? '✅' : type === 'danger' ? '❌' : 'ℹ️'}</span> ${message}`;
    document.body.appendChild(toast);
    setTimeout(() => { toast.style.opacity='0'; setTimeout(() => toast.remove(), 500); }, 3000);
}

// Password strength checker
function checkPasswordStrength(pw) {
    const bar = document.getElementById('pwStrength');
    if (!bar) return;
    let strength = 0;
    if (pw.length >= 8) strength++;
    if (/[A-Z]/.test(pw)) strength++;
    if (/[0-9]/.test(pw)) strength++;
    if (/[^A-Za-z0-9]/.test(pw)) strength++;
    const colors = ['#ef4444','#f59e0b','#3b82f6','#10b981'];
    const labels = ['Weak','Fair','Good','Strong'];
    bar.style.width = (strength * 25) + '%';
    bar.style.background = colors[strength-1] || '#ef4444';
    const label = document.getElementById('pwStrengthLabel');
    if (label) label.textContent = labels[strength-1] || '';
}

// Toggle password visibility
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    if (input) input.type = input.type === 'password' ? 'text' : 'password';
}

// Confirm action dialogs
function confirmDelete(msg) { return confirm(msg || 'Are you sure?'); }

// Mobile sidebar
function openSidebar() {
    document.getElementById('sidebar').classList.add('open');
}
