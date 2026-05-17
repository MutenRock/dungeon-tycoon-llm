
const HERO_ROSTER = [
    { id: 'h1', name: "Pierrick", class: "Chevalier", row: "front", hp: 120, maxHp: 120, atk: 18, def: 12, emoji: "🛡️" },
    { id: 'h2', name: "Yanskar", class: "Assassin", row: "front", hp: 80, maxHp: 80, atk: 25, def: 6, emoji: "🗡️" },
    { id: 'h3', name: "Amelios", class: "Mage", row: "back", hp: 60, maxHp: 60, atk: 22, def: 4, emoji: "🧙" },
    { id: 'h4', name: "Léorian", class: "Archer", row: "back", hp: 75, maxHp: 75, atk: 20, def: 7, emoji: "🏹" }
];

let combatState = {
    heroes: [],
    monsters: [],
    turnQueue: [],
    active: false,
    deadHeroesThisFight: []
};

function startCombat() {
    if(combatState.active) return;

    const availableMonsters = entities.filter(e => e.type === 'monster');
    if(availableMonsters.length === 0) {
        logCombat("Il faut des monstres dans la caserne pour combattre !");
        return;
    }

    combatState.active = true;
    combatState.deadHeroesThisFight = [];
    combatState.heroes = JSON.parse(JSON.stringify(HERO_ROSTER)); 

    combatState.monsters = availableMonsters.slice(0, 4).map((m, i) => ({
        id: 'm'+i, name: m.race, class: "Monstre", 
        row: i < 2 ? "front" : "back", 
        hp: m.hp, maxHp: STATS[m.race]?.hp || m.hp, 
        atk: m.atk, def: m.def, emoji: STATS[m.race]?.emoji || "👹"
    }));

    buildCombatArena();
    logCombat("⚔️ <b>DÉBUT DU COMBAT JRPG</b>");

    triggerHeroBark(combatState.heroes[0], "Le groupe entre dans la salle face aux monstres.");
    setTimeout(combatLoop, 2000);
}

function buildCombatArena() {
    const barracks = document.getElementById('barracks');
    barracks.innerHTML = `
        <div class="combat-arena">
            <div class="team-side heroes">
                <div class="combat-row back-row" id="hero-back"></div>
                <div class="combat-row front-row" id="hero-front"></div>
            </div>
            <div class="team-side monsters">
                <div class="combat-row front-row" id="monster-front"></div>
                <div class="combat-row back-row" id="monster-back"></div>
            </div>
        </div>
    `;
    updateArenaVisuals();
}

function updateArenaVisuals() {
    ['hero-back', 'hero-front', 'monster-front', 'monster-back'].forEach(id => document.getElementById(id).innerHTML = '');

    const renderEntity = (ent, side) => {
        if(ent.hp <= 0) return '';
        const hpPct = Math.max(0, (ent.hp / ent.maxHp) * 100);
        return `
            <div class="combat-entity ${side}" id="${ent.id}">
                <div class="hp-bar-container"><div class="hp-bar" style="width: ${hpPct}%; background: ${hpPct<30?'red':'#4caf50'}"></div></div>
                ${ent.emoji}
                <div class="name-tag">${ent.name}</div>
            </div>
        `;
    };

    combatState.heroes.forEach(h => {
        if(h.row === 'back') document.getElementById('hero-back').innerHTML += renderEntity(h, 'hero');
        else document.getElementById('hero-front').innerHTML += renderEntity(h, 'hero');
    });

    combatState.monsters.forEach(m => {
        if(m.row === 'front') document.getElementById('monster-front').innerHTML += renderEntity(m, 'monster');
        else document.getElementById('monster-back').innerHTML += renderEntity(m, 'monster');
    });
}

async function combatLoop() {
    if(!combatState.active) return;

    let aliveHeroes = combatState.heroes.filter(h => h.hp > 0);
    let aliveMonsters = combatState.monsters.filter(m => m.hp > 0);

    if(aliveHeroes.length === 0) { 
        logCombat("💀 <b>Victoire du Donjon !</b>"); 
        endJRPGCombat(true); 
        return; 
    }
    if(aliveMonsters.length === 0) { 
        logCombat("🏆 <b>Les Héros ont conquis la salle.</b>"); 
        triggerHeroBark(aliveHeroes[0], "Le groupe a survécu à ce terrible combat et célèbre.");

        // Save victory memory for survivors
        aliveHeroes.forEach(h => {
            let memory = "A survécu à une bataille sanglante dans la caserne.";
            if(combatState.deadHeroesThisFight.length > 0) {
                memory = `A survécu mais a vu mourir ses alliés : ${combatState.deadHeroesThisFight.join(', ')}.`;
            }
            saveHeroMemory(h.name, memory);
        });

        setTimeout(() => endJRPGCombat(false), 3000); 
        return; 
    }

    const isHeroTurn = Math.random() > 0.5;
    let attacker, defender;

    if(isHeroTurn) {
        attacker = aliveHeroes[Math.floor(Math.random() * aliveHeroes.length)];
        let targets = aliveMonsters.filter(m => m.row === 'front');
        if(targets.length === 0) targets = aliveMonsters;
        defender = targets[Math.floor(Math.random() * targets.length)];
    } else {
        attacker = aliveMonsters[Math.floor(Math.random() * aliveMonsters.length)];
        let targets = aliveHeroes.filter(h => h.row === 'front');
        if(targets.length === 0) targets = aliveHeroes;
        defender = targets[Math.floor(Math.random() * targets.length)];
    }

    executeAttack(attacker, defender, isHeroTurn);
}

function executeAttack(attacker, defender, isHeroAttacking) {
    const atkEl = document.getElementById(attacker.id);
    const defEl = document.getElementById(defender.id);

    if(atkEl) atkEl.classList.add(isHeroAttacking ? 'anim-attack-hero' : 'anim-attack-monster');
    setTimeout(() => { if(atkEl) atkEl.classList.remove('anim-attack-hero', 'anim-attack-monster'); }, 400);

    const dmg = Math.max(1, attacker.atk - defender.def);
    defender.hp -= dmg;

    if(defEl) defEl.classList.add('anim-damage');
    setTimeout(() => { if(defEl) defEl.classList.remove('anim-damage'); }, 300);

    logCombat(`${attacker.emoji} ${attacker.name} inflige <b>${dmg}</b> à ${defender.emoji} ${defender.name}.`);

    if(isHeroAttacking && (defender.hp <= 0 || dmg > 15 || Math.random() < 0.3)) {
        let event = `Tu viens d'attaquer ${defender.name}.`;
        if(defender.hp <= 0) event = `Tu viens de massacrer ${defender.name}.`;
        triggerHeroBark(attacker, event);
    } else if(!isHeroAttacking && defender.hp > 0 && dmg > 15) {
        triggerHeroBark(defender, `Le monstre ${attacker.name} vient de t'infliger une blessure grave.`);
    } else if(!isHeroAttacking && defender.hp <= 0) {
        // HÉROS MEURT
        combatState.deadHeroesThisFight.push(defender.name);
        logCombat(`☠️ <b>${defender.name} a été tué par un ${attacker.name} !</b>`);

        // Sauvegarder la mémoire de la mort
        saveHeroMemory(defender.name, `A été brutalement tué par un ${attacker.name}.`);

        const aliveAlly = combatState.heroes.find(h => h.hp > 0 && h.id !== defender.id);
        if(aliveAlly) {
            triggerHeroBark(aliveAlly, `Ton ami ${defender.name} vient de se faire tuer par un ${attacker.name} ! Réagis !`);
            saveHeroMemory(aliveAlly.name, `A vu ${defender.name} se faire tuer par un ${attacker.name}.`);
        }
    }

    updateArenaVisuals();
    setTimeout(combatLoop, 1500);
}

async function triggerHeroBark(hero, eventContext) {
    const el = document.getElementById(hero.id);
    if(!el) return;
    try {
        const res = await fetch('/api/chat/hero-bark', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ hero_name: hero.name, event: eventContext })
        });
        const data = await res.json();

        const old = el.querySelector('.combat-bubble');
        if(old) old.remove();

        const bubble = document.createElement('div');
        bubble.className = 'combat-bubble';
        bubble.innerText = data.bark;
        el.appendChild(bubble);
        setTimeout(() => bubble.remove(), 4000);
    } catch(e) {}
}

function saveHeroMemory(heroName, memoryText) {
    fetch('/api/heroes/memory', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ hero_name: heroName, memory: memoryText })
    });
}

function endJRPGCombat(monstersWin) {
    combatState.active = false;
    if(!monstersWin) {
        entities = entities.filter(e => e.type !== 'monster');
    }
    setTimeout(() => {
        document.getElementById('barracks').innerHTML = '';
        logCombat("<i>Fin de l'affrontement.</i>");
    }, 2000);
}
