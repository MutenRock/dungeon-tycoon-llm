/**
 * Dialogue system — advisor conversations with speech bubbles.
 */

function openDialogue(advisorId, advisorName) {
  gameState.dialogueTarget = advisorId;
  const panel = document.getElementById("dialogue-panel");
  const nameEl = document.getElementById("dialogue-npc-name");
  const messages = document.getElementById("dialogue-messages");

  if (panel) panel.classList.remove("hidden");
  if (nameEl) nameEl.textContent = advisorName;
  if (messages) messages.innerHTML = "";

  // Load history
  loadDialogueHistory(advisorId);
}

function closeDialogue() {
  gameState.dialogueTarget = null;
  const panel = document.getElementById("dialogue-panel");
  if (panel) panel.classList.add("hidden");
}

async function loadDialogueHistory(advisorId) {
  const data = await apiGet(`/api/dialogue/advisor/${advisorId}/history`);
  const messages = document.getElementById("dialogue-messages");
  if (!messages || !data?.history) return;

  messages.innerHTML = "";
  data.history.forEach((msg) => {
    addBubble(msg.role === "player" ? "player" : "npc", msg.content);
  });
}

async function sendDialogue() {
  const input = document.getElementById("dialogue-input");
  if (!input || !input.value.trim() || !gameState.dialogueTarget) return;

  const message = input.value.trim();
  input.value = "";

  addBubble("player", message);

  const result = await apiPost(`/api/dialogue/advisor/${gameState.dialogueTarget}/talk`, {
    message: message,
  });

  if (result?.response) {
    addBubble("npc", result.response, result.advisor_name);
  }

  if (result?.wish_resolved) {
    const wr = result.wish_resolved;
    const emoji = wr.success ? "✨" : "💀";
    addBubble("npc", `${emoji} [${wr.outcome}] Score: ${(wr.score * 100).toFixed(0)}%`, "System");
  }
}

function addBubble(role, text, speaker) {
  const messages = document.getElementById("dialogue-messages");
  if (!messages) return;

  const bubble = document.createElement("div");
  bubble.className = `speech-bubble ${role}`;

  if (speaker && role === "npc") {
    const sp = document.createElement("div");
    sp.className = "speaker";
    sp.textContent = speaker;
    bubble.appendChild(sp);
  }

  const content = document.createElement("div");
  content.textContent = text;
  bubble.appendChild(content);

  messages.appendChild(bubble);
  messages.scrollTop = messages.scrollHeight;
}

// Enter key sends dialogue
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("dialogue-input");
  if (input) {
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") sendDialogue();
    });
  }
});
