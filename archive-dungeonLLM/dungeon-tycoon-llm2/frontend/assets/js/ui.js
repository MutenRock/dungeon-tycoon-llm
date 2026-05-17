async function refreshState() {
  gameState.data = await apiGet("/game/state");
  renderGrid(gameState.data);
  renderPanels();
}

function renderPanels() {
  const state = gameState.data;
  if (!state) return;

  document.getElementById("resource-panel").textContent =
    `Wood: ${state.resources.wood}\nStone: ${state.resources.stone}\nMeat: ${state.resources.meat}`;

  document.getElementById("boss-status").textContent =
    `Day: ${state.day}\nPhase: ${state.phase}\nLives: ${state.lives}\nTreasure: ${state.treasure}`;

  document.getElementById("raid-log").textContent = (state.logs || []).slice(-12).join("\n");
}

document.getElementById("new-game-btn").addEventListener("click", async () => {
  gameState.data = await apiPost("/game/new");
  renderGrid(gameState.data);
  renderPanels();
});

document.getElementById("place-room-btn").addEventListener("click", async () => {
  const id = `room_${Math.floor(Math.random() * 100000)}`;
  const payload = {
    room_id: id,
    room_type: "corridor",
    x: Math.floor(Math.random() * 10),
    y: Math.floor(Math.random() * 10),
    w: 1,
    h: 1,
    doors: ["north", "south"]
  };
  const result = await apiPost("/grid/place-room", payload);
  if (!result.detail) {
    gameState.data = result;
    renderGrid(gameState.data);
    renderPanels();
  }
});

document.getElementById("night-btn").addEventListener("click", async () => {
  gameState.data = await apiPost("/turn/night/resolve");
  renderGrid(gameState.data);
  renderPanels();
});

window.addEventListener("DOMContentLoaded", refreshState);
