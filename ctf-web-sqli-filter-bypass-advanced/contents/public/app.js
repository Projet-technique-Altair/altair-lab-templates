const runBtn = document.getElementById("runBtn");
const output = document.getElementById("output");

runBtn.addEventListener("click", async () => {
  const id = document.getElementById("idInput").value;
  const resp = await fetch(`./api/mission?id=${encodeURIComponent(id)}`);
  const body = await resp.text();
  output.textContent = `${resp.status} ${resp.statusText}\n${body}`;
});
