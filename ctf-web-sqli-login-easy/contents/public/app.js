const loginBtn = document.getElementById("loginBtn");
const meBtn = document.getElementById("meBtn");
const flagBtn = document.getElementById("flagBtn");

const loginResult = document.getElementById("loginResult");
const apiResult = document.getElementById("apiResult");

async function toText(resp) {
  const body = await resp.text();
  return `${resp.status} ${resp.statusText}\n${body}`;
}

loginBtn.addEventListener("click", async () => {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const resp = await fetch("./api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  loginResult.textContent = await toText(resp);
});

meBtn.addEventListener("click", async () => {
  const resp = await fetch("./api/me");
  apiResult.textContent = await toText(resp);
});

flagBtn.addEventListener("click", async () => {
  const resp = await fetch("./api/flag");
  apiResult.textContent = await toText(resp);
});
