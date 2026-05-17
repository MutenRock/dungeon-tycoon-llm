
window.playerContext = { name: "Zargoth", race: "Démon", dungeonName: "Le Gouffre" };

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
}

function startIntro() {
    playerContext.name = document.getElementById('player-name').value || "Inconnu";

    // Clean race name from the "(Pack: ...)" text for the LLM context
    const rawRace = document.getElementById('player-race').value;
    playerContext.race = rawRace; 

    playerContext.dungeonName = `${document.getElementById('dungeon-word1').value} ${document.getElementById('dungeon-word2').value}`;
    document.getElementById('display-dungeon-name').innerText = playerContext.dungeonName;

    showScreen('screen-intro');
}

function startLoading() {
    showScreen('screen-loading');
    const texts = ["Ouverture des portes...", "Récupération de la récompense spéciale...", "Polissage du trône..."];
    let i = 0;
    const intv = setInterval(() => {
        i++;
        if(i < texts.length) document.getElementById('loading-text').innerText = texts[i];
        else {
            clearInterval(intv);
            showScreen('screen-game');
            initSim(); 
            setupInitialMonsters(); // Spawn de départ !
        }
    }, 1200);
}

function handleEnter(e) { if(e.key === 'Enter') sendMessage(); }
function unlockDungeon() {
    document.getElementById('btn-to-dungeon').classList.remove('hidden');
    document.querySelector('.chat-input-area').classList.add('hidden');
}

function setupInitialMonsters() {
    // 1. Pack de base selon la race
    const raceMap = {
        "Démon": ["Gobelin", "Gobelin", "Orc"],
        "Liche": ["Squelette", "Squelette", "Squelette", "Squelette"],
        "Vampire": ["Gobelin", "Squelette"],
        "Roi Gobelin": ["Gobelin", "Gobelin", "Gobelin", "Gobelin", "Gobelin"]
    };

    const initialPack = raceMap[window.playerContext.race] || ["Gobelin", "Gobelin"];
    initialPack.forEach(m => createEntity(m, 'monster'));

    // 2. Unité spéciale offerte par Lucifer
    if(window.specialReward && window.specialReward !== "none") {
        document.getElementById('reward-badge').innerText = "Cadeau de Lucifer : " + window.specialReward;
        logCombat(`🎁 Lucifer vous a envoyé un(e) <b>${window.specialReward}</b> !`);

        // Ajouter à la liste des spawns possibles si on veut
        const select = document.getElementById('spawn-race');
        const opt = document.createElement('option');
        opt.value = window.specialReward;
        opt.innerText = window.specialReward + " (Spécial)";
        select.appendChild(opt);

        // On crée l'entité visuellement en forçant des stats correctes
        createEntity(window.specialReward, 'monster', true); 
    }
}
