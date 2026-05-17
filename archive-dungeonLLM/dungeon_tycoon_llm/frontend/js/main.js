let state=null;let selectedRoom=null;let demolishMode=false;let pendingMonster=null;

document.addEventListener("DOMContentLoaded",()=>{
  initGrid(document.getElementById("dungeon-grid"),onCellClick);
  document.querySelectorAll(".room-btn").forEach(btn=>{
    btn.addEventListener("click",()=>{
      demolishMode=false;updateDemolishBtn(false);hidePendingMonster();
      if(selectedRoom?.room_type===btn.dataset.room){selectedRoom=null;btn.classList.remove("selected");setModeLabel("");}
      else{document.querySelectorAll(".room-btn").forEach(b=>b.classList.remove("selected"));btn.classList.add("selected");selectedRoom={room_type:btn.dataset.room,width:parseInt(btn.dataset.w),height:parseInt(btn.dataset.h)};setModeLabel(`Mode pose : ${btn.textContent.trim()}`);}
    });
  });
  document.querySelectorAll(".monster-btn").forEach(btn=>{
    btn.addEventListener("click",()=>{if(!pendingMonster)return;doAssign(pendingMonster.x,pendingMonster.y,btn.dataset.monster||null);hidePendingMonster();});
  });
  document.getElementById("btn-demolish").addEventListener("click",()=>{
    demolishMode=!demolishMode;selectedRoom=null;document.querySelectorAll(".room-btn").forEach(b=>b.classList.remove("selected"));updateDemolishBtn(demolishMode);setModeLabel(demolishMode?"Mode démolition — cliquez une salle":"");hidePendingMonster();
  });
  document.getElementById("btn-end-night").addEventListener("click",doEndNight);
  document.getElementById("btn-raid").addEventListener("click",doRaid);
  document.getElementById("btn-new").addEventListener("click",doNewGame);
  document.getElementById("btn-save").addEventListener("click",async()=>{try{await Api.save();addLog("Partie sauvegardée.");}catch(e){addLog("Erreur sauvegarde : "+e.message);}});
  document.getElementById("btn-load").addEventListener("click",doLoad);
  document.getElementById("btn-restart").addEventListener("click",()=>{hideGameOver();doNewGame();});
  Api.getGame().then(s=>applyState(s)).catch(()=>doNewGame());
});

async function onCellClick(x,y){if(!state||state.phase!=="night")return; if(demolishMode){try{const res=await Api.deleteRoom(x,y);addLog(res.message);applyState(res.state);}catch(e){addLog(e.message);}return;} if(selectedRoom){try{const res=await Api.placeRoom({x,y,...selectedRoom});addLog(res.message);applyState(res.state);}catch(e){addLog(e.message);}return;} const room=state.grid.find(r=>r.x<=x&&x<r.x+r.width&&r.y<=y&&y<r.y+r.height);if(room?.room_type==="monster_room"){pendingMonster={x:room.x,y:room.y};document.getElementById("monster-panel").style.display="block";document.getElementById("monster-target").textContent=`Assigner un monstre à (${room.x},${room.y})`;}}

async function doNewGame(){try{const s=await Api.newGame();clearLog();addLog("Nouvelle partie démarrée. Construisez votre donjon !");applyState(s);}catch(e){addLog(e.message);}}
async function doEndNight(){try{const res=await Api.endNight();addLog(res.message);applyState(res.state);}catch(e){addLog(e.message);}}
async function doRaid(){const btn=document.getElementById("btn-raid");btn.disabled=true;btn.textContent="⏳ Raid en cours…";try{const result=await Api.startRaid();const s=await Api.getGame();applyState(s);renderRaidLog(result);}catch(e){addLog(e.message);}finally{btn.disabled=false;btn.textContent="⚔ Lancer le raid";}}
async function doAssign(x,y,monsterType){try{const res=await Api.assign({x,y,monster_type:monsterType||null});addLog(res.message);applyState(res.state);}catch(e){addLog(e.message);}}
async function doLoad(){try{const s=await Api.load();clearLog();addLog("Partie chargée.");applyState(s);}catch(e){addLog(e.message);}}
function applyState(s){if(!s)return;state=s;renderGrid(state.grid);updateHUD(state);}function setModeLabel(text){document.getElementById("grid-mode-label").textContent=text;}function updateDemolishBtn(active){document.getElementById("btn-demolish").classList.toggle("btn-demolish-active",active);}function hidePendingMonster(){pendingMonster=null;document.getElementById("monster-panel").style.display="none";}
