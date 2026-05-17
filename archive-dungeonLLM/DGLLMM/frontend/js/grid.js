const GRID_SIZE = 10;
const ROOM_ICONS = { corridor:"⬜", monster_room:"👹", trap_room:"⚡", treasure_room:"💎", boss_room:"💀" };
const MONSTER_ICONS = { goblin:"🐾", skeleton:"💀", orc:"🗡", troll:"🧌" };
let _gridEl = null; let _onCellClick = null;
function initGrid(containerEl, onCellClick) {
  _gridEl = containerEl; _onCellClick = onCellClick; _gridEl.innerHTML = "";
  for (let y=0;y<GRID_SIZE;y++) for (let x=0;x<GRID_SIZE;x++) {
    const cell = document.createElement("div");
    cell.className = "cell"; cell.dataset.x=x; cell.dataset.y=y;
    cell.addEventListener("click", () => _onCellClick(x,y));
    _gridEl.appendChild(cell);
  }
}
function _getCell(x,y){return _gridEl?.querySelector(`[data-x="${x}"][data-y="${y}"]`);} 
function renderGrid(rooms){
  for(let y=0;y<GRID_SIZE;y++)for(let x=0;x<GRID_SIZE;x++){const c=_getCell(x,y);if(!c)continue;c.className="cell";c.textContent="";}
  for(const room of rooms){
    for(let dx=0;dx<room.width;dx++)for(let dy=0;dy<room.height;dy++){
      const c=_getCell(room.x+dx,room.y+dy);if(!c)continue;c.classList.add(room.room_type);
      if(dx===0&&dy===0){c.textContent=ROOM_ICONS[room.room_type]||"?";
        if(room.monster){const b=document.createElement("span");b.className="badge";b.textContent=MONSTER_ICONS[room.monster]||"?";c.appendChild(b);} }
    }
  }
}
