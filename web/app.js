console.log("app.js loaded");

// ---------- Create workspace ----------
const createBtn = document.getElementById("createBtn");
const result = document.getElementById("result");

createBtn.addEventListener("click", async () => {
    const token = document.getElementById("tokencreate").value.trim();
    const label = document.getElementById("label").value.trim();

    if (token.length < 4) {
        result.textContent = "Token must be at least 4 characters";
        return;
    }

    const response = await fetch("/api/workspaces", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: token,
            label: label
        })
    });

    if (!response.ok) {
        const errorData = await response.json();
        result.textContent = errorData.detail;
        return;
    }

    const data = await response.json();
    result.textContent = JSON.stringify(data, null, 2);
});

// ---------- Open workspace ----------
const openBtn = document.getElementById("openBtn");
const openResult = document.getElementById("openResult");

openBtn.addEventListener("click", async () => {
    const token = document.getElementById("tokenopen").value.trim();

    if (token.length < 4) {
        openResult.textContent = "Token must be at least 4 characters";
        return;
    }

    const response = await fetch(`/api/workspaces/${token}`);

    if (!response.ok) {
        const errorData = await response.json();
        openResult.textContent = errorData.detail;
        return;
    }

    const data = await response.json();

    localStorage.setItem("workspace_id", data.id);
    localStorage.setItem("workspace_token", data.token);
    localStorage.setItem("workspace_label", data.label);

    openResult.textContent = `Opened drawer: ${data.label || data.token}`;
});

// ---------- Save Feedback ----------

const saveBtn = document.getElementById("saveFeedbackBtn");
const saveResult = document.getElementById("saveFeedbackResult");

saveBtn.addEventListener("click", async () => {

    const workspaceId = localStorage.getItem("workspace_id");

    if (!workspaceId) {
        saveResult.textContent = "Open a drawer first.";
        return;
    }

    const text = document.getElementById("feedbackText").value.trim();
    const source = document.getElementById("feedbackSource").value.trim();
    const context = document.getElementById("feedbackContext").value.trim();
    const entry_type = document.getElementById("feedbackType").value.trim();

    if (!text) {
        saveResult.textContent = "Feedback text cannot be empty.";
        return;
    }

    const response = await fetch(`/api/workspaces/${workspaceId}/feedback`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: text,
            source: source,
            context: context,
            entry_type: entry_type
        })
    });

    if (!response.ok) {
        const errorData = await response.json();
        saveResult.textContent = errorData.detail;
        return;
    }

    const data = await response.json();

    saveResult.textContent = `Saved feedback id: ${data.feedback_id}`;
});

// ---------- Analyze strengths ----------

const analyzeBtn = document.getElementById("analyzeBtn");
const analyzeResult = document.getElementById("analyzeResult");

analyzeBtn.addEventListener("click", async () => {
    const workspaceId = localStorage.getItem("workspace_id");

    if (!workspaceId) {
        analyzeResult.textContent = "Open a drawer first.";
        return;
    }

    const response = await fetch(`/api/workspaces/${workspaceId}/analyze`, {
        method: "POST"
    });

    if (!response.ok) {
        const errorData = await response.json();
        analyzeResult.textContent = errorData.detail;
        return;
    }

    const data = await response.json();

    analyzeResult.innerHTML = data.strengths
    .map((strength, index) => `
        <p><strong>${index + 1}. ${strength.name}</strong><br>${strength.reason}</p>
    `)
    .join("");
});