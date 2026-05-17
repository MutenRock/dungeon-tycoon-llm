document.getElementById("raid-btn").addEventListener("click", async () => {
  const result = await apiPost("/turn/day/start-raid");
  gameState.raid = result;
  document.getElementById("raid-log").textContent = (result.logs || []).join("\n");
  await refreshState();
});
