const createBtn = document.getElementById("createBtn")
const result = document.getElementById("result")

createBtn.addEventListener("click", async () => {
    const token = document.getElementById("token").value
    const label = document.getElementById("label").value

    const response = await fetch("/api/workspace", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: token,
            label: label
        })
    })

    const data = await response.json()

    result.textContent = JSON.stringify(data, null, 2)
})

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