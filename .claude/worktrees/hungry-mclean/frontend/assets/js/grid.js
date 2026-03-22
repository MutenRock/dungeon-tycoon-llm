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

async function onCellClick(x, y, existingRoom) {
  if (existingRoom) {
    // Right-click or shift-click could remove — for now just log
    console.log("Room exists:", existingRoom);
    return;
  }

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
