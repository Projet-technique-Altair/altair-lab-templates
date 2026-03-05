const express = require("express");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = process.env.PORT || 3000;

const UNLOCK_CODE = "STATION-ALTAIR";
const FLAG_PATH = "/opt/flag/flag.txt";

app.use(express.urlencoded({ extended: false }));
app.use(express.json());
app.use("/public", express.static(path.join(__dirname, "public")));

function isUnlocked(req) {
  const cookieHeader = req.headers.cookie || "";
  return cookieHeader.split(";").some((pair) => pair.trim() === "unlocked=1");
}

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.post("/unlock", (req, res) => {
  const code = String(req.body.code || "");
  if (code === UNLOCK_CODE) {
    res.setHeader("Set-Cookie", "unlocked=1; Path=/");
    return res.json({ ok: true });
  }
  return res.status(401).json({ ok: false });
});

app.post("/diagnose", (req, res) => {
  if (!isUnlocked(req)) {
    return res.status(403).json({ ok: false, error: "Console locked" });
  }

  const expression = String(req.body.expression || "");

  // Intentionally vulnerable: user-controlled eval() for CTF purposes.
  try {
    const result = eval(expression);
    return res.json({ ok: true, result });
  } catch (err) {
    return res.status(400).json({ ok: false, error: String(err) });
  }
});

app.get("/flag-location", (req, res) => {
  // Hint route that points to the flag file when you can read it.
  res.type("text/plain").send(FLAG_PATH);
});

if (require.main === module) {
  if (!fs.existsSync(FLAG_PATH)) {
    console.warn(`Flag file not found at ${FLAG_PATH}`);
  }
  app.listen(PORT, () => {
    console.log(`Orbital station console running on :${PORT}`);
  });
}

module.exports = app;
