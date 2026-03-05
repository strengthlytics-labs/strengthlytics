const out = document.querySelector("#out");

document.querySelector("#btnHealth").addEventListener("click", async () => {
  const res = await fetch("/api/health");
  const data = await res.json();
  out.textContent = JSON.stringify(data, null, 2);
});