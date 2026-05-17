
let chatHistory = [];
let turnCount = 0;
const MAX_TURNS = 3; // On raccourcit l'intro
window.specialReward = null;

async function sendMessage() {
    const input = document.getElementById('chat-input'); 
    const msg = input.value.trim();
    if(!msg) return;

    // 1. Ajouter le message du joueur et le garder
    appendMsg('player', msg); 
    input.value = '';

    // 2. Ajouter un NOUVEAU bloc pour le chargement de Lucifer
    const loadingId = appendMsg('lucifer', '<span class="loading-dots">...</span>');

    try {
        const res = await fetch('/api/chat/lucifer', {
            method: 'POST', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ 
                message: msg, 
                history: chatHistory,
                player_context: window.playerContext
            })
        });

        const data = await res.json();

        // 3. Remplacer UNIQUEMENT le bloc de chargement par la réponse de Lucifer
        document.getElementById(loadingId).innerHTML = data.reply;

        // Sauvegarder la récompense si elle existe (au dernier tour)
        if(data.reward && data.reward !== "none") {
            window.specialReward = data.reward;
        }

        chatHistory.push({role: 'user', content: msg}, {role: 'assistant', content: data.reply});
        turnCount++;

        if(turnCount >= MAX_TURNS) {
            unlockDungeon();
        }

    } catch(e) {
        document.getElementById(loadingId).innerText = "[Erreur de connexion avec les Enfers]";
    }
}

function appendMsg(role, text) {
    const h = document.getElementById('chat-history');
    const id = 'msg-' + Date.now() + Math.floor(Math.random()*1000);

    const msgDiv = document.createElement('div');
    msgDiv.id = id;
    msgDiv.className = `msg ${role}`;
    msgDiv.innerHTML = text;

    h.appendChild(msgDiv);
    h.scrollTop = h.scrollHeight;

    return id;
}
