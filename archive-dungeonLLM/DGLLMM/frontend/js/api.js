const API_BASE = "http://127.0.0.1:8000";
async function apiFetch(method, path, body = null) {
  const opts = { method, headers: { "Content-Type": "application/json" } };
  if (body !== null) opts.body = JSON.stringify(body);
  const res = await fetch(API_BASE + path, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}
const Api = {
  newGame:    ()      => apiFetch("POST", "/game/new"),
  getGame:    ()      => apiFetch("GET",  "/game"),
  placeRoom:  (body)  => apiFetch("POST", "/game/room",  body),
  deleteRoom: (x, y)  => apiFetch("DELETE", `/game/room/${x}/${y}`),
  assign:     (body)  => apiFetch("POST", "/game/assign", body),
  endNight:   ()      => apiFetch("POST", "/game/end-night"),
  startRaid:  ()      => apiFetch("POST", "/raid/start"),
  save:       ()      => apiFetch("POST", "/game/save"),
  load:       ()      => apiFetch("POST", "/game/load"),
};
