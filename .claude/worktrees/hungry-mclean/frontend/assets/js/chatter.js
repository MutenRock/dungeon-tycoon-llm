/**
 * Monster chatter overlay — ambient dialogue from dungeon creatures.
 */

let chatterInterval = null;

async function fetchChatter() {
  const overlay = document.getElementById("chatter-overlay");
  if (!overlay) return;

  try {
    const data = await apiGet("/api/dialogue/chatter");
    if (data?.lines?.length) {
      overlay.classList.remove("hidden");
      overlay.innerHTML = data.lines
        .map((line) => `<p>${line}</p>`)
        .join("");

      // Auto-hide after 8 seconds
      setTimeout(() => {
        overlay.classList.add("hidden");
      }, 8000);
    }
  } catch (e) {
    // Silently fail — chatter is non-essential
  }
}

function startChatter() {
  // Fetch chatter every 30 seconds
  if (chatterInterval) clearInterval(chatterInterval);
  chatterInterval = setInterval(fetchChatter, 30000);
  // Initial fetch after 5 seconds
  setTimeout(fetchChatter, 5000);
}

function stopChatter() {
  if (chatterInterval) {
    clearInterval(chatterInterval);
    chatterInterval = null;
  }
}

document.addEventListener("DOMContentLoaded", startChatter);
