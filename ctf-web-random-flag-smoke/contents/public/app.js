const output = document.querySelector("#output");
const refreshButton = document.querySelector("#refreshButton");

function print(value) {
  output.textContent =
    typeof value === "string" ? value : JSON.stringify(value, null, 2);
}

async function requestJson(path, options) {
  const response = await fetch(path, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok) {
    throw data;
  }
  return data;
}

async function loadFlag() {
  try {
    const data = await requestJson("api/flag");
    print(data.flag || data);
  } catch (error) {
    print(error);
  }
}

refreshButton.addEventListener("click", loadFlag);
loadFlag();
