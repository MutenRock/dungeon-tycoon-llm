function updateHUD(state){
  document.getElementById("hud-turn").textContent=state.turn;
  document.getElementById("hud-lives-val").textContent=state.boss_lives;
  document.getElementById("hud-treasure-val").textContent=state.treasure;
  document.getElementById("res-wood").textContent=state.resources.wood;
  document.getElementById("res-stone").textContent=state.resources.stone;
  document.getElementById("res-meat").textContent=state.resources.meat;
  const phaseEl=document.getElementById("hud-phase");
  const isNight=state.phase==="night";
  phaseEl.textContent=isNight?`🌙 Nuit — Tour ${state.turn}`:`☀ Jour — Tour ${state.turn}`;
  phaseEl.className="hud-pill "+(isNight?"phase-night":"phase-day");
  document.getElementById("btn-end-night").style.display=isNight?"block":"none";
  document.getElementById("btn-raid").style.display=isNight?"none":"block";
}
function addLog(text,type="info"){const log=document.getElementById("log");const e=document.createElement("div");e.className="log-entry";e.textContent=text;log.appendChild(e);log.scrollTop=log.scrollHeight;}
function clearLog(){document.getElementById("log").innerHTML="";hideNarrative();}
function showNarrative(text){const box=document.getElementById("narrative-box");document.getElementById("narrative-text").textContent=text;box.style.display="block";}
function hideNarrative(){document.getElementById("narrative-box").style.display="none";}
function showGameOver(){document.getElementById("overlay-gameover").style.display="flex";}
function hideGameOver(){document.getElementById("overlay-gameover").style.display="none";}
function renderRaidLog(result){clearLog();for(const ev of result.events){addLog(ev.description,ev.event_type);}const outcome=result.heroes_won?`⚔ Le boss est tombé ! (${result.boss_lives_remaining} vie(s) restante(s)) — Trésor perdu : ${result.treasure_stolen}`:`🛡 Le donjon a résisté — Trésor perdu : ${result.treasure_stolen}`;addLog(outcome);if(result.narrative)showNarrative(result.narrative);if(result.game_over)showGameOver();}
