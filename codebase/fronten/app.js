const DEFAULT_API_URL = "http://localhost:8001";

const elements = {
  apiUrl: document.querySelector("#api-url"),
  clearChat: document.querySelector("#clear-chat"),
  connectionCheck: document.querySelector("#connection-check"),
  form: document.querySelector("#chat-form"),
  messages: document.querySelector("#messages"),
  question: document.querySelector("#question"),
  sendButton: document.querySelector("#send-button"),
  slideContext: document.querySelector("#slide-context"),
  slidePage: document.querySelector("#slide-page"),
  statusDot: document.querySelector("#status-dot"),
  statusLabel: document.querySelector("#status-label"),
  topStatusDot: document.querySelector("#top-status-dot"),
  topStatusLabel: document.querySelector("#top-status-label"),
};

function apiBaseUrl() {
  return elements.apiUrl.value.trim().replace(/\/+$/, "") || DEFAULT_API_URL;
}

function setHealthState(isOnline) {
  [elements.statusDot, elements.topStatusDot].forEach((dot) => {
    dot.classList.toggle("online", isOnline);
    dot.classList.toggle("offline", !isOnline);
  });
  elements.statusLabel.textContent = isOnline ? "Backend online" : "Backend offline";
  elements.topStatusLabel.textContent = isOnline ? "Đã kết nối" : "Mất kết nối";
  elements.connectionCheck.classList.toggle("online", isOnline);
}

async function checkHealth() {
  try {
    const response = await fetch(`${apiBaseUrl()}/health`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    setHealthState(true);
  } catch {
    setHealthState(false);
  }
}

function addUserMessage(text) {
  elements.messages.insertAdjacentHTML("beforeend", `
    <div class="message user">
      <div class="message-body">
        <div class="message-text">${escapeHtml(text)}</div>
        <div class="message-meta">Bạn · vừa xong</div>
      </div>
      <div class="message-avatar">U</div>
    </div>`);
}

function addTypingMessage() {
  const node = document.createElement("div");
  node.className = "message";
  node.id = "typing-message";
  node.innerHTML = `<div class="message-avatar">✦</div><div class="message-body"><div class="message-text typing"><i></i><i></i><i></i></div></div>`;
  elements.messages.appendChild(node);
  scrollMessages();
}

function renderResponse(data) {
  const badgeClass = `case-${String(data.case || "").toLowerCase()}`;
  const citation = data.citation?.has_citation && data.citation.exact_quote
    ? `<div class="response-detail"><div class="detail-label">Citation · ${escapeHtml(data.citation.source || "Nguồn")}</div><div class="detail-value">“${escapeHtml(data.citation.exact_quote)}”</div></div>`
    : "";
  const clarification = data.clarification_question
    ? `<div class="response-detail"><div class="detail-label">Câu hỏi làm rõ</div><div class="detail-value">${escapeHtml(data.clarification_question)}</div></div>`
    : "";
  const hint = data.next_action_hint
    ? `<div class="response-detail"><div class="detail-label">Gợi ý tiếp theo</div><div class="detail-value">${escapeHtml(data.next_action_hint)}</div></div>`
    : "";
  const node = document.createElement("div");
  node.className = "message";
  node.innerHTML = `
    <div class="message-avatar">✦</div>
    <div class="message-body">
      <div class="response-meta"><span class="case-badge ${badgeClass}">${escapeHtml(data.case || "?")}</span><span class="action-label">${formatAction(data.action)}</span></div>
      <div class="message-text">${escapeHtml(data.reply_text || "Backend không trả về nội dung.")}</div>
      ${citation}${clarification}${hint}
      <div class="message-meta">Grounded Tutor · vừa xong</div>
    </div>`;
  elements.messages.appendChild(node);
}

function addErrorMessage(error) {
  const node = document.createElement("div");
  node.className = "message";
  node.innerHTML = `<div class="message-avatar">!</div><div class="message-body"><div class="message-text error-message">${escapeHtml(error)}</div><div class="message-meta">Không thể hoàn tất request</div></div>`;
  elements.messages.appendChild(node);
}

async function sendQuestion(event) {
  event.preventDefault();
  const question = elements.question.value.trim();
  if (!question || elements.sendButton.disabled) return;

  document.querySelector("#welcome-card")?.remove();
  addUserMessage(question);
  addTypingMessage();
  elements.question.value = "";
  elements.sendButton.disabled = true;
  elements.sendButton.innerHTML = "Đang gửi... <span>•</span>";
  scrollMessages();

  try {
    const response = await fetch(`${apiBaseUrl()}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_input: question,
        slide_context: elements.slideContext.value.trim(),
        slide_page: Number(elements.slidePage.value) || 1,
      }),
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok) throw new Error(payload?.detail || `Backend trả về HTTP ${response.status}`);
    setHealthState(true);
    renderResponse(payload);
  } catch (error) {
    setHealthState(false);
    const message = error instanceof TypeError
      ? "Không kết nối được backend. Hãy kiểm tra backend port 8001 và CORS."
      : error.message;
    addErrorMessage(message);
  } finally {
    document.querySelector("#typing-message")?.remove();
    elements.sendButton.disabled = false;
    elements.sendButton.innerHTML = "Gửi câu hỏi <span>→</span>";
    scrollMessages();
  }
}

function clearChat() {
  elements.messages.innerHTML = `<div class="welcome-card" id="welcome-card"><div class="welcome-icon">✦</div><h3>Sẵn sàng kiểm thử</h3><p>Nhập câu hỏi về nội dung slide. Mình sẽ gửi request tới backend và hiển thị rõ nguồn dẫn, case cùng hướng xử lý.</p><div class="quick-prompts"><button type="button" data-prompt="Data Lake là gì?">Data Lake là gì?</button><button type="button" data-prompt="Cái này là gì?">Cần hỏi lại</button><button type="button" data-prompt="Deadline bài tập tuần này?">Ngoài phạm vi</button></div></div>`;
  bindQuickPrompts();
}

function bindQuickPrompts() {
  document.querySelectorAll("[data-prompt]").forEach((button) => {
    button.addEventListener("click", () => {
      elements.question.value = button.dataset.prompt;
      elements.question.focus();
    });
  });
}

function formatAction(action) {
  return { ANSWER_WITH_CITATION: "TRẢ LỜI CÓ NGUỒN", ASK_CLARIFICATION: "HỎI LÀM RÕ", REFUSE_AND_GUIDE: "TỪ CHỐI & HƯỚNG DẪN" }[action] || action || "RESPONSE";
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[char]));
}

function scrollMessages() {
  elements.messages.scrollTop = elements.messages.scrollHeight;
}

elements.form.addEventListener("submit", sendQuestion);
elements.clearChat.addEventListener("click", clearChat);
document.querySelector("#refresh-health").addEventListener("click", checkHealth);
elements.apiUrl.addEventListener("change", checkHealth);
elements.question.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    elements.form.requestSubmit();
  }
});
bindQuickPrompts();
checkHealth();
