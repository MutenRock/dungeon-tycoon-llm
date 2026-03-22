/**
 * Raid result display with hero dialogue bubbles.
 */

function renderRaidResult(result) {
  const el = document.getElementById("raid-log-content");
  if (!el || !result) return;

  let html = "";

  // Raid header
  html += `<p><strong>Day ${result.day} Raid</strong> — ${result.heroes?.length || 0} heroes</p>`;
  html += `<p>${result.success ? "⚠️ Heroes reached the boss!" : "✅ Dungeon defended!"}</p>`;
  html += `<p>Treasure: ${result.treasure_delta > 0 ? "+" : ""}${result.treasure_delta}</p>`;

  // Hero dialogue
  if (result.hero_dialogue?.length) {
    html += `<div style="margin: 8px 0;">`;
    result.hero_dialogue.forEach((line) => {
      html += `<div class="hero-speech">${line}</div>`;
    });
    html += `</div>`;
  }

  // Combat logs
  if (result.logs?.length) {
    result.logs.forEach((log) => {
      html += `<p>${log}</p>`;
    });
  }

  // Survivors
  if (result.survivors?.length) {
    html += `<p><strong>Survivors:</strong> ${result.survivors.map((h) => h.name).join(", ")}</p>`;
  }

  el.innerHTML = html;
}
