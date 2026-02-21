/**
 * script.js — GCIQS frontend logic.
 *
 * Handles: query submission, SSE streaming from the backend,
 * rendering references, error states, and basic UX niceties.
 */

// Use same origin — works on Vercel (same domain) and localhost
const API_BASE = window.location.origin;

// ── DOM refs ──────────────────────────────────────────────

const queryInput    = document.getElementById("queryInput");
const submitBtn     = document.getElementById("submitBtn");
const resultsSection = document.getElementById("resultsSection");
const loader        = document.getElementById("loader");
const errorBox      = document.getElementById("errorBox");
const errorMsg      = document.getElementById("errorMsg");
const answerPanel   = document.getElementById("answerPanel");
const answerContent = document.getElementById("answerContent");
const referencesPanel = document.getElementById("referencesPanel");
const refsGrid      = document.getElementById("refsGrid");
const statusDot     = document.getElementById("statusDot");
const statusText    = document.getElementById("statusText");

// ── health check on load ──────────────────────────────────

async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE}/health`);
        if (res.ok) {
            const data = await res.json();
            statusDot.classList.add("ok");
            statusDot.classList.remove("err");
            statusText.textContent = `online · ${data.index_size} docs indexed`;
        } else {
            throw new Error("unhealthy");
        }
    } catch (e) {
        statusDot.classList.add("err");
        statusDot.classList.remove("ok");
        statusText.textContent = "backend offline";
    }
}

// run health check on page load, then every 30s
checkHealth();
setInterval(checkHealth, 30000);

// ── example query chips ───────────────────────────────────

function fillExample(el) {
    queryInput.value = el.textContent.trim();
    queryInput.focus();
}

// ── submit query ──────────────────────────────────────────

async function submitQuery() {
    const query = queryInput.value.trim();
    if (!query) return;

    // reset UI
    resetResults();
    resultsSection.classList.add("visible");
    loader.classList.add("active");
    submitBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/query`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, top_k: 5 }),
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.error || `HTTP ${response.status}`);
        }

        // read SSE stream
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        let firstToken = true;

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });

            // SSE messages are separated by double newlines
            const lines = buffer.split("\n\n");
            buffer = lines.pop(); // keep incomplete chunk

            for (const line of lines) {
                if (!line.startsWith("data: ")) continue;
                const payload = line.slice(6); // strip "data: "

                let msg;
                try {
                    msg = JSON.parse(payload);
                } catch {
                    continue;
                }

                handleSSEMessage(msg, firstToken);
                if (msg.type === "token" && firstToken) {
                    firstToken = false;
                }
            }
        }

        // handle any remaining buffer
        if (buffer.startsWith("data: ")) {
            try {
                const msg = JSON.parse(buffer.slice(6));
                handleSSEMessage(msg, false);
            } catch { /* ignore partial */ }
        }

    } catch (err) {
        showError(err.message);
    } finally {
        submitBtn.disabled = false;
        loader.classList.remove("active");
        answerContent.classList.remove("streaming");
    }
}

function handleSSEMessage(msg, firstToken) {
    switch (msg.type) {
        case "references":
            renderReferences(msg.data);
            break;

        case "token":
            if (firstToken) {
                loader.classList.remove("active");
                answerPanel.classList.add("active");
                answerContent.classList.add("streaming");
            }
            answerContent.textContent += msg.data;
            // auto-scroll if user hasn't scrolled up
            answerContent.scrollTop = answerContent.scrollHeight;
            break;

        case "error":
            showError(msg.data);
            break;

        case "done":
            answerContent.classList.remove("streaming");
            // post-process: highlight [DOC-XXX] citations
            highlightCitations();
            break;
    }
}

// ── render references ─────────────────────────────────────

function renderReferences(refs) {
    if (!refs || refs.length === 0) return;

    refsGrid.innerHTML = "";
    referencesPanel.classList.add("active");

    for (const ref of refs) {
        const card = document.createElement("div");
        card.className = "ref-card";
        card.dataset.id = ref.id;

        const citationsHtml = (ref.references || [])
            .map(r => `<div class="ref-citation">• ${escapeHtml(r)}</div>`)
            .join("");

        card.innerHTML = `
            <span class="ref-id">${ref.id}</span>
            <div class="ref-body">
                <div class="ref-title">${escapeHtml(ref.title)}</div>
                <div class="ref-meta">
                    <span class="gene-tag">${escapeHtml(ref.gene || "multi")}</span>
                    <span class="type-tag">${escapeHtml(ref.type)}</span>
                </div>
                ${citationsHtml ? `<div class="ref-citations">${citationsHtml}</div>` : ""}
            </div>
            <span class="ref-score">score: ${ref.score}</span>
        `;

        refsGrid.appendChild(card);
    }
}

// ── highlight [DOC-XXX] citations in the answer ───────────

function highlightCitations() {
    const raw = answerContent.textContent;
    // replace [DOC-001] style refs with styled spans
    const html = escapeHtml(raw).replace(
        /\[(DOC-\d+)\]/g,
        '<span class="cite">[$1]</span>'
    );
    answerContent.innerHTML = html;
}

// ── copy answer to clipboard ──────────────────────────────

async function copyAnswer() {
    const text = answerContent.textContent;
    if (!text) return;
    try {
        await navigator.clipboard.writeText(text);
        // brief visual feedback
        const btn = document.querySelector(".copy-btn");
        btn.style.color = "var(--accent)";
        btn.style.borderColor = "var(--accent)";
        setTimeout(() => {
            btn.style.color = "";
            btn.style.borderColor = "";
        }, 1200);
    } catch {
        // fallback for older browsers
        const ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
    }
}

// ── helpers ───────────────────────────────────────────────

function resetResults() {
    errorBox.classList.remove("active");
    answerPanel.classList.remove("active");
    referencesPanel.classList.remove("active");
    answerContent.textContent = "";
    answerContent.classList.remove("streaming");
    refsGrid.innerHTML = "";
}

function showError(message) {
    loader.classList.remove("active");
    errorBox.classList.add("active");
    errorMsg.textContent = message;
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

// ── keyboard shortcut: Ctrl+Enter to submit ───────────────

queryInput.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        submitQuery();
    }
});