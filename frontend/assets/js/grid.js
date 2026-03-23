/**
 * Grid renderer — displays the 10x10 dungeon grid with room types.
 */
function renderGrid(state) {
  const grid = document.getElementById("grid");
  if (!grid) return;
  grid.innerHTML = "";

  // Build occupied map: "x,y" -> room
  const occupied = {};
  if (state?.dungeon?.rooms) {
    state.dungeon.rooms.forEach((room) => {
      for (let dx = 0; dx < room.w; dx++) {
        for (let dy = 0; dy < room.h; dy++) {
          occupied[`${room.x + dx},${room.y + dy}`] = room;
        }
      }
    });
  }

  for (let y = 0; y < 10; y++) {
    for (let x = 0; x < 10; x++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      cell.dataset.x = x;
      cell.dataset.y = y;

      const room = occupied[`${x},${y}`];
      if (room) {
        cell.classList.add(`room-${room.type}`);
        cell.title = `${room.type} (${room.id})`;
      }

      cell.addEventListener("click", () => onCellClick(x, y, room));
      grid.appendChild(cell);
    }
  }
}

let selectedRoomRef = null;

function showRoomDetails(room) {
  selectedRoomRef = room;
  const panel = document.getElementById("room-details");
  const content = document.getElementById("room-details-content");
  if (!panel || !content) return;

  // Find monsters assigned to this room
  const monsters = (gameState.data?.monsters || []).filter(
    (m) => m.room_id === room.id
  );
  const monsterList = monsters.length
    ? monsters.map((m) => m.name || m.type).join(", ")
    : "None";

  let html = `
    <p><strong>Type:</strong> ${room.type.replace("_", " ")}</p>
    <p><strong>Position:</strong> (${room.x}, ${room.y})</p>
    <p><strong>Size:</strong> ${room.w}x${room.h}</p>
  `;
  if (room.type === "trap_room" && room.trap_type) {
    html += `<p><strong>Trap:</strong> ${room.trap_type}</p>`;
  }
  html += `<p><strong>Monsters:</strong> ${monsterList}</p>`;

  content.innerHTML = html;
  panel.classList.remove("hidden");
}

function hideRoomDetails() {
  selectedRoomRef = null;
  const panel = document.getElementById("room-details");
  if (panel) panel.classList.add("hidden");
}

async function removeSelectedRoom() {
  if (!selectedRoomRef) return;
  const result = await apiPost("/api/grid/remove-room", { room_id: selectedRoomRef.id });
  hideRoomDetails();
  await refreshState();
}

async function onCellClick(x, y, existingRoom) {
  if (existingRoom) {
    showRoomDetails(existingRoom);
    return;
  }

  // Hide details panel when clicking empty cell
  hideRoomDetails();

  // Place selected room type
  const roomType = gameState.selectedRoom || "corridor";
  const result = await apiPost("/api/grid/place-room", {
    room_type: roomType,
    x: x,
    y: y,
    w: roomType === "boss_room" || roomType === "barracks" ? 2 : 1,
    h: 1,
  });

  if (result.success) {
    await refreshState();
  } else {
    console.warn("Place failed:", result.error);
  }
}
