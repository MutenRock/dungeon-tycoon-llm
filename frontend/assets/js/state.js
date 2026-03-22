/**
 * Global game state — single source of truth on the client side.
 */
const gameState = {
  data: null,       // PlayerState from backend
  raid: null,       // Latest RaidResult
  selectedRoom: "corridor",
  language: "en",
  dialogueTarget: null, // advisor ID for active dialogue
};

async function refreshState() {
  gameState.data = await apiGet("/api/game/state");
  renderAll();
}

function renderAll() {
  if (!gameState.data) return;
  renderGrid(gameState.data);
  renderResources(gameState.data);
  renderAdvisors(gameState.data);
  renderStatusBar(gameState.data);
  renderLog(gameState.data);
}
