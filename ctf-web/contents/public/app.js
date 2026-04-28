const unlockBtn = document.getElementById("unlockBtn");
const unlockStatus = document.getElementById("unlockStatus");
const consoleCard = document.getElementById("consoleCard");
const runBtn = document.getElementById("runBtn");
const result = document.getElementById("result");

const downlinkPayload = "U1RBVElPTi1BTFRBSVI=";

function setStatus(message, ok) {
  unlockStatus.textContent = message;
  unlockStatus.className = ok ? "status ok" : "status";
}

unlockBtn.addEventListener("click", async () => {
  const code = document.getElementById("accessCode").value.trim();
  const res = await fetch("./unlock", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code })
  });

  if (res.ok) {
    setStatus("Console unlocked.", true);
    consoleCard.classList.remove("locked");
  } else {
    setStatus("Access denied.", false);
  }
});

runBtn.addEventListener("click", async () => {
  const expression = document.getElementById("expression").value.trim();
  result.textContent = "Running...";

  const res = await fetch("./diagnose", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expression })
  });

  const payload = await res.json();
  if (!res.ok) {
    result.textContent = `Error: ${payload.error}`;
    return;
  }

  result.textContent = `Result: ${payload.result}`;
});

// Comms downlink beacon for the gate.
// eslint-disable-next-line no-console
console.log(`Downlink payload: ${downlinkPayload}`);
