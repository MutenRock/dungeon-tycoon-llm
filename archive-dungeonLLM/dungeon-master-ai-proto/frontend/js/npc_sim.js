
const barracks = document.getElementById('barracks');
const combatLog = document.getElementById('combat-log');
let entities = [];
let simInterval;
let inCombat = false;

const STATS = {
    "Gobelin": { hp: 30, atk: 10, def: 2, emoji: "👺" },
    "Squelette": { hp: 40, atk: 12, def: 4, emoji: "💀" },
    "Orc": { hp: 70, atk: 18, def: 6, emoji: "👹" },
    "Chevalier": { hp: 100, atk: 15, def: 10, emoji: "🛡️" },
    "Mage": { hp: 40, atk: 25, def: 5, emoji: "🧙" },
    "Archer": { hp: 60, atk: 20, def: 5, emoji: "🏹" }
};

function initSim() {
    if(simInterval) clearInterval(simInterval);
    simInterval = setInterval(updateSim, 500);
}

function spawnMonster() {
    const race = document.getElementById('spawn-race').value;
    createEntity(race, 'monster');
}

function createEntity(race, type, isSpecial=false) {
    const el = document.createElement('div');
    el.className = `entity ${type} ${isSpecial ? 'special-unit' : ''}`;

    // Si c'est une unité inventée par l'IA, on lui donne des stats par défaut
    let entStats = STATS[race];
    if(!entStats) {
        entStats = { hp: 80, atk: 25, def: 8, emoji: "🔥" };
        STATS[race] = entStats; // Save for later
    }

    el.innerText = entStats.emoji;

    const x = Math.random() * (barracks.clientWidth - 30);
    const y = Math.random() * (barracks.clientHeight - 30);
    el.style.left = x + 'px';
    el.style.top = y + 'px';

    barracks.appendChild(el);
    entities.push({ id: Math.random(), el, race, type, x, y, hp: entStats.hp, ...entStats, cooldown: 0 });
    if(!isSpecial) logCombat(`[Spawn] Un ${race} rejoint la zone.`);
}

function updateSim() {
    if(inCombat) return;
    entities.forEach(ent => {
        if(ent.type !== 'monster') return;
        ent.x += (Math.random() - 0.5) * 40;
        ent.y += (Math.random() - 0.5) * 40;
        ent.x = Math.max(0, Math.min(barracks.clientWidth - 30, ent.x));
        ent.y = Math.max(0, Math.min(barracks.clientHeight - 30, ent.y));
        ent.el.style.left = ent.x + 'px';
        ent.el.style.top = ent.y + 'px';
        if(ent.cooldown > 0) ent.cooldown--;
    });

    for(let i=0; i<entities.length; i++) {
        for(let j=i+1; j<entities.length; j++) {
            const e1 = entities[i]; const e2 = entities[j];
            if(e1.cooldown > 0 || e2.cooldown > 0) continue;

            const dist = Math.hypot(e1.x - e2.x, e1.y - e2.y);
            if(dist < 40) {
                triggerDialogue(e1, e2);
                e1.cooldown = 20; e2.cooldown = 20;
            }
        }
    }
}

async function triggerDialogue(e1, e2) {
    showBubble(e1, "...");
    showBubble(e2, "...");
    try {
        const res = await fetch('/api/chat/npc-encounter', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ race1: e1.race, race2: e2.race })
        });
        const data = await res.json();
        showBubble(e1, data.npc1_text);
        setTimeout(() => showBubble(e2, data.npc2_text), 2000);
    } catch(e) {
        showBubble(e1, "Grmbl...");
    }
}

function showBubble(ent, text) {
    const old = ent.el.querySelector('.bubble');
    if(old) old.remove();
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.innerText = text;
    ent.el.appendChild(bubble);
    setTimeout(() => bubble.remove(), 4000);
}

