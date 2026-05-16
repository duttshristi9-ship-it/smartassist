// SmartAssist Chat JavaScript
const messagesArea = document.getElementById('messagesArea');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');
const intentDisplay = document.getElementById('intentDisplay');

let isWaiting = false;

// Auto-resize textarea
chatInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Send on Enter (Shift+Enter for newline)
chatInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (!isWaiting) sendMessage();
    }
});

chatForm.addEventListener('submit', function(e) {
    e.preventDefault();
    if (!isWaiting) sendMessage();
});

function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    appendMessage('user', text, new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'}));
    chatInput.value = '';
    chatInput.style.height = 'auto';
    setWaiting(true);
    showTyping();
    scrollToBottom();

    fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: text})
    })
    .then(r => r.json())
    .then(data => {
        hideTyping();
        if (data.success) {
            appendMessage('ai', data.response, data.timestamp, data.intent, data.severity, data.confidence);
            updateIntentDisplay(data);
            if (data.needs_escalation) showEscalationAlert(data.disaster_type);
            addHistoryItem(text, data.intent);
        } else {
            appendMessage('ai', '⚠️ Sorry, I encountered an error. Please try again.', new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'}));
        }
    })
    .catch(() => {
        hideTyping();
        appendMessage('ai', '⚠️ Connection error. Please check your network and try again.', new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'}));
    })
    .finally(() => setWaiting(false));
}

function appendMessage(role, text, time, intent, severity, confidence) {
    const isUser = role === 'user';
    const row = document.createElement('div');
    row.className = `msg-row ${isUser ? 'user-msg' : ''}`;

    const formattedText = formatMarkdown(text);
    const intentBadge = (intent && intent !== 'general' && !isUser)
        ? `<span class="intent-tag">🎯 ${intent.replace(/_/g,' ')}</span>` : '';
    const sevBadge = (severity && !isUser)
        ? `<span class="severity-tag sev-${severity}">${severity}</span>` : '';
    const confText = (confidence && !isUser)
        ? `<span style="color:var(--text-muted);font-size:10px">AI ${Math.round(confidence*100)}%</span>` : '';

    row.innerHTML = `
        <div class="msg-avatar ${isUser ? 'user' : 'ai'}">${isUser ? '👤' : '🤖'}</div>
        <div class="msg-content">
            <div class="msg-bubble ${isUser ? 'user' : 'ai'}">${formattedText}</div>
            <div class="msg-meta">
                <span>${time}</span>
                ${intentBadge}${sevBadge}${confText}
            </div>
        </div>`;

    messagesArea.appendChild(row);
    scrollToBottom();
}

function formatMarkdown(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^#{1,4}\s+(.+)$/gm, '<h4>$1</h4>')
        .replace(/^•\s+(.+)$/gm, '<li>$1</li>')
        .replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/gs, m => `<ul>${m}</ul>`)
        .replace(/\n{2,}/g, '<br><br>')
        .replace(/\n/g, '<br>')
        .replace(/`([^`]+)`/g, '<code style="background:rgba(255,255,255,.08);padding:2px 6px;border-radius:4px;font-family:monospace">$1</code>');
}

function showTyping() { typingIndicator.style.display = 'flex'; scrollToBottom(); }
function hideTyping() { typingIndicator.style.display = 'none'; }
function setWaiting(v) { isWaiting = v; sendBtn.disabled = v; }
function scrollToBottom() { messagesArea.scrollTop = messagesArea.scrollHeight; }

function updateIntentDisplay(data) {
    if (!intentDisplay) return;
    intentDisplay.innerHTML = `
        <div style="font-size:11px;color:var(--text-muted);margin-bottom:4px">Last Detection</div>
        <div style="font-size:20px;margin-bottom:4px">${data.icon || '💬'}</div>
        <div style="font-size:13px;font-weight:600">${data.disaster_type}</div>
        <div class="badge badge-${data.severity || 'low'}" style="margin-top:6px">${data.severity || 'low'}</div>`;
}

function showEscalationAlert(disasterType) {
    const banner = document.getElementById('escalationBanner');
    if (banner) {
        banner.querySelector('.escalation-type').textContent = disasterType;
        banner.style.display = 'flex';
        setTimeout(() => banner.style.display = 'none', 8000);
    }
}

function addHistoryItem(text, intent) {
    const list = document.getElementById('historyList');
    if (!list) return;
    const item = document.createElement('div');
    item.className = 'history-item';
    item.innerHTML = `<div>${text.substring(0, 40)}${text.length > 40 ? '...' : ''}</div>
        <div class="h-intent">${intent.replace(/_/g,' ')}</div>`;
    list.insertBefore(item, list.firstChild);
}

function clearChat() {
    if (!confirm('Clear all chat history?')) return;
    fetch('/api/chat/clear', {method:'POST'})
        .then(r => r.json())
        .then(() => { messagesArea.innerHTML = ''; document.getElementById('historyList').innerHTML = ''; });
}

function useQuickPrompt(text) {
    chatInput.value = text;
    chatInput.focus();
}

// Emergency SOS button
function triggerSOS() {
    const modal = document.getElementById('sosModal');
    if (modal) modal.style.display = 'flex';
}
function closeSOS() {
    const modal = document.getElementById('sosModal');
    if (modal) modal.style.display = 'none';
}

// Scroll to bottom on load
scrollToBottom();
