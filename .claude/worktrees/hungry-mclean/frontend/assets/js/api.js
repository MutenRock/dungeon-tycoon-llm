/**
 * API client — all backend communication goes through here.
 */
const API_BASE = "http://localhost:8000";

async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`);
  return res.json();
}

async function apiPost(path, body = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res.json();
}
