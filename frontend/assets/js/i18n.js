/**
 * Minimal i18n — loads strings from backend and applies to [data-i18n] elements.
 */

const i18nStrings = {
  en: {
    resources: "Resources",
    rooms: "Rooms",
    advisors: "Advisors",
    raid_log: "Raid Log",
    log: "Log",
    resolve_night: "Resolve Night",
    start_raid: "Start Raid",
    save_pattern: "Save Pattern",
    save_game: "Save Game",
  },
  fr: {
    resources: "Ressources",
    rooms: "Salles",
    advisors: "Conseillers",
    raid_log: "Journal de Raid",
    log: "Journal",
    resolve_night: "Résoudre la Nuit",
    start_raid: "Lancer le Raid",
    save_pattern: "Sauver le Patron",
    save_game: "Sauvegarder",
  },
};

function applyI18n(lang) {
  const strings = i18nStrings[lang] || i18nStrings.en;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (strings[key]) {
      el.textContent = strings[key];
    }
  });
}

function toggleLanguage() {
  gameState.language = gameState.language === "en" ? "fr" : "en";
  applyI18n(gameState.language);
}

document.addEventListener("DOMContentLoaded", () => {
  applyI18n(gameState.language || "en");
});
