
const grid = document.getElementById('grid');
let gridData = Array(100).fill('E');

function initGrid() {
    for(let i=0; i<98; i++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.onclick = () => {
            if(cell.classList.contains('room')) { cell.classList.remove('room'); cell.classList.add('trap'); gridData[i]='T'; }
            else if(cell.classList.contains('trap')) { cell.classList.remove('trap'); gridData[i]='E'; }
            else { cell.classList.add('room'); gridData[i]='R'; }
            console.log("Donjon compressé :", gridData.map((v, idx) => v !== 'E' ? `${idx}:${v}` : '').filter(Boolean).join(','));
        };
        grid.appendChild(cell);
    }
    const boss = document.createElement('div'); boss.className = 'cell boss'; boss.innerHTML = '<b>BOSS</b>';
    grid.appendChild(boss);
}
initGrid();
