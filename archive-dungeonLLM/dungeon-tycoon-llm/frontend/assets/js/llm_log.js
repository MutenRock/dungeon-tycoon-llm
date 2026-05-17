async function refreshDailySummary() {
  const result = await apiPost("/llm/daily-summary");
  document.getElementById("daily-summary").textContent = result.summary;
}

window.addEventListener("DOMContentLoaded", refreshDailySummary);
