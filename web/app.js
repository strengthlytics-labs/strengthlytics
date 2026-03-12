// Hitta knappen med id="createBtn" i HTML
const createBtn = document.getElementById("createBtn");

// Hitta rutan där vi vill visa svaret från servern
const result = document.getElementById("result");

// Lyssna på klick på Create-knappen
createBtn.addEventListener("click", async () => {

    // Hämta det användaren har skrivit i token-fältet
    const token = document.getElementById("token").value.trim();

    // Hämta det användaren har skrivit i label-fältet
    const label = document.getElementById("label").value;

    if (token.length < 4) {
    result.textContent = "Token must be at least 4 characters"
    return
  }

    // Skicka en HTTP request till backend
    const response = await fetch("/api/workspace", {

        // Vi skickar data för att skapa något nytt
        method: "POST",

        // Tala om för backend att datan vi skickar är JSON
        headers: {
            "Content-Type": "application/json"
        },

        // Själva datan vi skickar till backend
        // JSON.stringify gör om ett JS-objekt till JSON-text
        body: JSON.stringify({
            token: token,
            label: label
        })
    });

    // Läs svaret från backend som JSON
    const data = await response.json();

    // Visa svaret snyggt i <pre id="result">
    result.textContent = JSON.stringify(data, null, 2);
});