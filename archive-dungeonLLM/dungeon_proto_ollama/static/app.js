
// --- 1. Génération de la Grille 10x10 ---
const grid = document.getElementById('grid');
let gridData = Array(100).fill('E'); // E = Empty

function initGrid() {
    for(let i=0; i<98; i++) { // 98 cases + 1 case Boss (qui prend 2 espaces)
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.index = i;
        cell.onclick = () => toggleCell(cell, i);
        grid.appendChild(cell);
    }
    // Salle du Boss (2x1)
    const bossCell = document.createElement('div');
    bossCell.className = 'cell boss';
    bossCell.innerHTML = '<span style="display:flex; justify-content:center; align-items:center; height:100%; font-weight:bold;">BOSS</span>';
    grid.appendChild(bossCell);
}

function toggleCell(cell, index) {
    // Cycle simple: Empty -> Room -> Trap -> Empty
    if(cell.classList.contains('room')) {
        cell.classList.remove('room');
        cell.classList.add('trap');
        gridData[index] = 'T';
    } else if(cell.classList.contains('trap')) {
        cell.classList.remove('trap');
        gridData[index] = 'E';
    } else {
        cell.classList.add('room');
        gridData[index] = 'R';
    }
    console.log("Dungeon State Compressed:", compressDungeon());
}

// Compression basique pour le LLM
function compressDungeon() {
    return gridData.map((val, i) => val !== 'E' ? `${i}:${val}` : '').filter(Boolean).join(',');
}

initGrid();

// --- 2. Heavy LLM : Chat HTTP ---
let chatHistory = [];
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const msg = input.value.trim();
    if(!msg) return;

    appendMessage('player', msg);
    input.value = '';

    try {
        const response = await fetch('/api/chat/lucifer', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ message: msg, history: chatHistory })
        });
        const data = await response.json();

        appendMessage('lucifer', data.reply);
        document.getElementById('wish-score').innerText = data.hidden_wish_score;

        chatHistory.push({ role: 'user', content: msg });
        chatHistory.push({ role: 'assistant', content: data.reply });
    } catch(err) {
        console.error("Erreur Chat:", err);
    }
}

function appendMessage(role, text) {
    const historyDiv = document.getElementById('chat-history');
    const msgDiv = document.createElement('div');
    msgDiv.className = `msg ${role}`;
    msgDiv.innerText = text;
    historyDiv.appendChild(msgDiv);
    historyDiv.scrollTop = historyDiv.scrollHeight;
}

// --- 3. Fast LLM : WebSockets (Barks d'ambiance) ---
const ws = new WebSocket(`ws://${location.host}/ws/background-chat`);
const barksContainer = document.getElementById('floating-barks');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    barksContainer.innerHTML = `💬 <strong>${data.npc} :</strong> "${data.msg}"`;
    // Efface le bark après 4 secondes
    setTimeout(() => { barksContainer.innerHTML = ''; }, 4000);
};
