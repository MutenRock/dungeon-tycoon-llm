
// Etat global du joueur
window.playerContext = {
    name: "Zargoth",
    race: "Démon",
    dungeonName: "Le Gouffre Oublié"
};

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
}

function startIntro() {
    // Récupérer les données du formulaire
    playerContext.name = document.getElementById('player-name').value || "Inconnu";
    playerContext.race = document.getElementById('player-race').value;

    const w1 = document.getElementById('dungeon-word1').value;
    const w2 = document.getElementById('dungeon-word2').value;
    playerContext.dungeonName = `${w1} ${w2}`;

    // Mettre à jour le nom du donjon dans l'interface de jeu
    document.getElementById('display-dungeon-name').innerText = playerContext.dungeonName;

    // Lancer l'écran d'intro
    showScreen('screen-intro');

    // Initialiser le premier message système pour l'historique (côté front)
    console.log("Contexte initialisé :", playerContext);
}

function handleEnter(e) {
    if(e.key === 'Enter') sendMessage();
}

function unlockDungeon() {
    document.getElementById('btn-to-dungeon').classList.remove('hidden');
    document.querySelector('.chat-input-area').classList.add('hidden');
}
