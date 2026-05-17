const API_BASE = "http://127.0.0.1:8000/api";

async function apiGet(path) {
  const response = await fetch(`${API_BASE}${path}`);
  return response.json();
}

async function apiPost(path, payload = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return response.json();
}
