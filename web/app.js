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