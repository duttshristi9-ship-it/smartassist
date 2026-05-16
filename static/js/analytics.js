// SmartAssist Analytics Dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadAnalytics();
});

const COLORS_INTENT = ['#3b82f6','#ef4444','#f59e0b','#10b981','#8b5cf6','#06b6d4','#ec4899','#f97316'];
const COLORS_SEV = {'Critical':'#ef4444','High':'#f59e0b','Medium':'#3b82f6','Low':'#10b981'};

function loadAnalytics() {
    fetch('/api/analytics/overview')
        .then(r => r.json())
        .then(data => {
            updateSummaryCards(data.summary);
            renderIntentChart(data.intent_distribution);
            renderDailyChart(data.daily_activity);
            renderSeverityChart(data.severity_distribution);
            renderReportChart(data.report_by_type);
            renderStatusChart(data.report_status);
            renderUserTrend(data.user_trend);
        })
        .catch(() => console.error('Failed to load analytics'));
}

function updateSummaryCards(s) {
    const map = {
        'statQueries': s.total_queries,
        'statUsers': s.total_users,
        'statReports': s.total_reports,
        'statCritical': s.critical_cases,
        'statEscalated': s.escalated,
        'statOpen': s.open_reports
    };
    for (const [id, val] of Object.entries(map)) {
        const el = document.getElementById(id);
        if (el) animateCounter(el, val);
    }
}

function animateCounter(el, target) {
    let current = 0;
    const step = Math.max(1, Math.ceil(target / 40));
    const timer = setInterval(() => {
        current = Math.min(current + step, target);
        el.textContent = current.toLocaleString();
        if (current >= target) clearInterval(timer);
    }, 30);
}

function renderIntentChart(data) {
    const ctx = document.getElementById('intentChart');
    if (!ctx || !data.labels.length) return;
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{data: data.data, backgroundColor: COLORS_INTENT, borderWidth: 0, hoverOffset: 8}]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: {position:'right', labels:{color:'#94a3b8', font:{size:12}, boxWidth:12}},
                tooltip: {callbacks:{label: c => ` ${c.label}: ${c.raw} queries`}}
            }
        }
    });
}

function renderDailyChart(data) {
    const ctx = document.getElementById('dailyChart');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Queries', data: data.data,
                borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,0.1)',
                fill: true, tension: 0.4, pointBackgroundColor: '#3b82f6', pointRadius: 4
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {legend:{display:false}},
            scales: {
                x:{grid:{color:'rgba(255,255,255,0.05)'},ticks:{color:'#94a3b8'}},
                y:{grid:{color:'rgba(255,255,255,0.05)'},ticks:{color:'#94a3b8'},beginAtZero:true}
            }
        }
    });
}

function renderSeverityChart(data) {
    const ctx = document.getElementById('severityChart');
    if (!ctx || !data.labels.length) return;
    const colors = data.labels.map(l => COLORS_SEV[l] || '#6b7280');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{label:'Cases', data:data.data, backgroundColor:colors.map(c=>c+'33'), borderColor:colors, borderWidth:2, borderRadius:8}]
        },
        options: {
            responsive:true, maintainAspectRatio:false,
            plugins:{legend:{display:false}},
            scales:{
                x:{grid:{display:false},ticks:{color:'#94a3b8'}},
                y:{grid:{color:'rgba(255,255,255,0.05)'},ticks:{color:'#94a3b8'},beginAtZero:true}
            }
        }
    });
}

function renderReportChart(data) {
    const ctx = document.getElementById('reportTypeChart');
    if (!ctx || !data.labels.length) return;
    new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: data.labels,
            datasets: [{data:data.data, backgroundColor:COLORS_INTENT.map(c=>c+'88'), borderWidth:0}]
        },
        options: {
            responsive:true, maintainAspectRatio:false,
            plugins:{legend:{position:'right',labels:{color:'#94a3b8',font:{size:11},boxWidth:10}}}
        }
    });
}

function renderStatusChart(data) {
    const ctx = document.getElementById('statusChart');
    if (!ctx || !data.labels.length) return;
    const colors = ['#ef4444','#f59e0b','#10b981','#6b7280'];
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{data:data.data, backgroundColor:colors, borderWidth:0, hoverOffset:6}]
        },
        options: {
            responsive:true, maintainAspectRatio:false,
            plugins:{legend:{position:'bottom',labels:{color:'#94a3b8',font:{size:11},boxWidth:10}}}
        }
    });
}

function renderUserTrend(data) {
    const ctx = document.getElementById('userTrendChart');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label:'New Users', data:data.data,
                backgroundColor:'rgba(16,185,129,0.3)', borderColor:'#10b981', borderWidth:2, borderRadius:6
            }]
        },
        options: {
            responsive:true, maintainAspectRatio:false,
            plugins:{legend:{display:false}},
            scales:{
                x:{grid:{display:false},ticks:{color:'#94a3b8'}},
                y:{grid:{color:'rgba(255,255,255,0.05)'},ticks:{color:'#94a3b8'},beginAtZero:true}
            }
        }
    });
}

function refreshAnalytics() {
    const btn = document.getElementById('refreshBtn');
    if (btn) { btn.innerHTML = '<span class="loader"></span>'; }
    loadAnalytics();
    setTimeout(() => { if (btn) btn.innerHTML = '🔄 Refresh'; }, 1500);
}
