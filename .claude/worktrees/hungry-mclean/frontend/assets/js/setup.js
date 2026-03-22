/**
 * Setup wizard — game creation flow with species selection, naming, and Lucifer intro.
 */

const setupState = {
  species: "goblin",
  dungeonName: "",
  advisorRace: "goblin",
  language: "en",
  luciferStep: 0,
  luciferExchanges: [],
  currentQuestion: "",
};

// --- Navigation ---

function nextStep(step) {
  document.querySelectorAll(".wizard-step").forEach((el) => el.classList.remove("active"));
  const target = document.getElementById(`step-${step}`);
  if (target) target.classList.add("active");

  if (step === 4) startLucifer();
}

// --- Step 1: Species ---

async function loadSpecies() {
  const data = await apiGet("/api/setup/bestiary");
  const grid = document.getElementById("species-grid");
  if (!grid || !Array.isArray(data)) return;

  grid.innerHTML = "";
  data.forEach((species) => {
    const card = document.createElement("div");
    card.className = `species-card${species.species_id === setupState.species ? " selected" : ""}`;
    card.innerHTML = `
      <h4>${species.name}</h4>
      <p>${species.description}</p>
      <div class="traits">${species.traits.map((t) => `<span class="trait-tag">${t}</span>`).join("")}</div>
    `;
    card.onclick = () => {
      setupState.species = species.species_id;
      document.querySelectorAll(".species-card").forEach((c) => c.classList.remove("selected"));
      card.classList.add("selected");
    };
    grid.appendChild(card);
  });
}

// --- Step 2: Dungeon Name ---

async function loadDungeonNames() {
  const data = await apiGet("/api/setup/dungeon-names");
  const container = document.getElementById("name-themes");
  if (!container || !data?.themes) return;

  container.innerHTML = "";
  data.themes.forEach((theme) => {
    const group = document.createElement("div");
    group.className = "theme-group";
    group.innerHTML = `<h4>${theme.theme}</h4>`;

    const names = theme.names_en || [];
    names.forEach((name) => {
      const opt = document.createElement("div");
      opt.className = "name-option";
      opt.textContent = name;
      opt.onclick = () => selectName(name);
      group.appendChild(opt);
    });

    container.appendChild(group);
  });
}

function selectName(name) {
  setupState.dungeonName = name;
  document.getElementById("selected-name-display").textContent = name;
  document.querySelectorAll(".name-option").forEach((el) => el.classList.remove("selected"));
  event.target.classList.add("selected");
}

// --- Step 3: Advisor Race ---

async function loadRaces() {
  const data = await apiGet("/api/setup/races");
  const grid = document.getElementById("race-grid");
  if (!grid || !data?.races) return;

  grid.innerHTML = "";
  data.races.forEach((race) => {
    const card = document.createElement("div");
    card.className = `race-card${race === setupState.advisorRace ? " selected" : ""}`;
    card.innerHTML = `<h4>${race}</h4>`;
    card.onclick = () => {
      setupState.advisorRace = race;
      document.querySelectorAll(".race-card").forEach((c) => c.classList.remove("selected"));
      card.classList.add("selected");
    };
    grid.appendChild(card);
  });
}

// --- Step 4: Lucifer ---

async function startLucifer() {
  const data = await apiPost("/api/setup/lucifer/start", {}, `?language=${setupState.language}`);
  if (data?.question) {
    setupState.luciferStep = 1;
    setupState.currentQuestion = data.question;
    addLuciferMessage("question", data.question);
  }
}

async function answerLucifer() {
  const input = document.getElementById("lucifer-input");
  if (!input || !input.value.trim()) return;

  const answer = input.value.trim();
  input.value = "";
  addLuciferMessage("answer", answer);

  const result = await apiPost("/api/setup/lucifer/respond", {
    step: setupState.luciferStep,
    question: setupState.currentQuestion,
    answer: answer,
    previous_exchanges: setupState.luciferExchanges,
    language: setupState.language,
  });

  if (result?.exchange) {
    setupState.luciferExchanges.push(result.exchange);
  }

  setupState.luciferStep++;

  if (result?.next_question) {
    setupState.currentQuestion = result.next_question;
    setTimeout(() => addLuciferMessage("question", result.next_question), 500);
  }

  if (result?.complete) {
    document.getElementById("lucifer-input-area").classList.add("hidden");
    document.getElementById("start-game-btn").classList.remove("hidden");
  }
}

function addLuciferMessage(type, text) {
  const container = document.getElementById("lucifer-messages");
  if (!container) return;
  const msg = document.createElement("div");
  msg.className = `lucifer-msg ${type}`;
  msg.textContent = text;
  container.appendChild(msg);
  container.scrollTop = container.scrollHeight;
}

// --- Start Game ---

async function startGame() {
  const name = setupState.dungeonName || document.getElementById("custom-name")?.value || "The Unnamed Depths";

  await apiPost("/api/setup/create-game", {
    dungeon_name: name,
    monster_species: setupState.species,
    advisor_race: setupState.advisorRace,
    player_race: "demon",
    language: setupState.language,
  });

  window.location.href = "index.html";
}

// --- Init ---

document.addEventListener("DOMContentLoaded", () => {
  loadSpecies();
  loadDungeonNames();
  loadRaces();
});
