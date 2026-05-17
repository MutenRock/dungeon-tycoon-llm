function renderGrid(state) {
  const grid = document.getElementById("grid");
  grid.innerHTML = "";

  const occupied = new Set();
  if (state?.dungeon?.rooms) {
    state.dungeon.rooms.forEach((room) => {
      for (let dx = 0; dx < room.w; dx++) {
        for (let dy = 0; dy < room.h; dy++) {
          occupied.add(`${room.x + dx},${room.y + dy}`);
        }
      }
    });
  }

  for (let y = 0; y < 10; y++) {
    for (let x = 0; x < 10; x++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      if (occupied.has(`${x},${y}`)) {
        cell.classList.add("room");
      }
      grid.appendChild(cell);
    }
  }
}
