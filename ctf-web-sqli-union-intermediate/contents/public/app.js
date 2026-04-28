const btn = document.getElementById("searchBtn");
const out = document.getElementById("output");

btn.addEventListener("click", async () => {
  const q = document.getElementById("q").value;
  const resp = await fetch(`./api/search?q=${encodeURIComponent(q)}`);
  const body = await resp.text();
  out.textContent = `${resp.status} ${resp.statusText}\n${body}`;
});
