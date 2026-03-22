/**
 * UI rendering — resource panel, advisor list, room palette, status bar, log.
 */

const ROOM_ICONS = {
  corridor: "🚪",
  monster_room: "👹",
  trap_room: "⚠️",
  treasure_room: "💎",
  boss_room: "👑",
  bonus_room: "🎁",
  barracks: "⚔️",
  kitchen: "🍖",
  workshop: "🔨",
  prison: "🔒",
};

function renderResources(state) {
  const el = document.getElementById("resources-list");
  if (!el || !state?.resources) return;
  el.innerHTML = `
    <div class="resource-row"><span>🪵 Wood</span><span>${state.resources.wood}</span></div>
    <div class="resource-row"><span>🪨 Stone</span><span>${state.resources.stone}</span></div>
    <div class="resource-row"><span>🥩 Meat</span><span>${state.resources.meat}</span></div>
    <div class="resource-row"><span>🥬 Vegetables</span><span>${state.resources.vegetables}</span></div>
    <div class="resource-row"><span>💰 Gold</span><span>${state.resources.gold}</span></div>
  `;
}

function renderAdvisors(state) {
  const el = document.getElementById("advisor-list");
  if (!el || !state?.advisors) return;
  el.innerHTML = "";

  state.advisors.forEach((adv) => {
    const sheet = state.character_registry?.find((s) => s.id === adv.character_sheet_id);
    const name = sheet?.name || adv.role;
    const item = document.createElement("div");
    item.className = "advisor-item";
    item.textContent = `${name} (${adv.role})`;
    item.onclick = () => openDialogue(adv.id, name);
    el.appendChild(item);
  });
}

function renderStatusBar(state) {
  const day = document.getElementById("day-display");
  const phase = document.getElementById("phase-display");
  const lives = document.getElementById("lives-display");
  const treasure = document.getElementById("treasure-display");
  const title = document.getElementById("dungeon-title");

  if (day) day.textContent = `Day ${state.day}`;
  if (phase) phase.textContent = state.phase.charAt(0).toUpperCase() + state.phase.slice(1);
  if (lives) lives.textContent = "❤".repeat(state.lives) + "🖤".repeat(3 - state.lives);
  if (treasure) treasure.textContent = `💰 ${state.treasure}`;
  if (title && state.game_config?.dungeon_name) {
    title.textContent = state.game_config.dungeon_name;
  }
}

function renderLog(state) {
  const el = document.getElementById("log-content");
  if (!el || !state?.logs) return;
  el.innerHTML = state.logs
    .slice(-20)
    .reverse()
    .map((l) => `<p>${l}</p>`)
    .join("");
}

function renderRoomPalette() {
  const el = document.getElementById("palette-list");
  if (!el) return;
  el.innerHTML = "";

  Object.entries(ROOM_ICONS).forEach(([type, icon]) => {
    const item = document.createElement("div");
    item.className = `palette-item${gameState.selectedRoom === type ? " selected" : ""}`;
    item.innerHTML = `<span>${icon}</span> ${type.replace("_", " ")}`;
    item.onclick = () => {
      gameState.selectedRoom = type;
      renderRoomPalette();
    };
    el.appendChild(item);
  });
}

// Button handlers
document.addEventListener("DOMContentLoaded", () => {
  renderRoomPalette();

  const nightBtn = document.getElementById("night-btn");
  if (nightBtn) {
    nightBtn.addEventListener("click", async () => {
      await apiPost("/api/turn/night/resolve");
      await refreshState();
    });
  }

  const raidBtn = document.getElementById("raid-btn");
  if (raidBtn) {
    raidBtn.addEventListener("click", async () => {
      const result = await apiPost("/api/turn/day/start-raid");
      gameState.raid = result;
      renderRaidResult(result);
      await refreshState();
    });
  }

  const saveBtn = document.getElementById("save-btn");
  if (saveBtn) {
    saveBtn.addEventListener("click", async () => {
      await apiPost("/api/game/save");
    });
  }

  const patternBtn = document.getElementById("save-pattern-btn");
  if (patternBtn) {
    patternBtn.addEventListener("click", async () => {
      const name = prompt("Pattern name:");
      if (name) {
        await apiPost("/api/patterns/save", { name });
      }
    });
  }

  // Load game state
  refreshState();
});
