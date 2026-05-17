# Dungeon Tycoon LLM

Prototype de jeu web où le joueur incarne le maître d'un donjon.
La nuit, il construit, assigne ses monstres et gère ses ressources.
Le jour, des héros attaquent le donjon pour atteindre la salle du boss et voler le trésor.

## Objectif du prototype
Créer une base propre, modulaire et versionnable pour développer rapidement un MVP jouable.

## Boucle de jeu MVP
1. **Nuit**
   - placer des salles sur une grille 10x10
   - consulter et gérer les ressources
   - assigner les monstres disponibles
2. **Jour**
   - générer un groupe de héros
   - simuler son parcours dans le donjon
   - résoudre pièges, combats et progression
3. **Résolution**
   - gain/perte de trésor
   - perte de vie du boss si les héros gagnent
   - journal narratif LLM

## Règles MVP
- Grille : 10x10
- Salle du boss : 2x1
- 3 vies au total
- Mort 1 : perte de 25% du trésor
- Mort 2 : perte de 50% du trésor
- Mort 3 : fin de partie
- Ressources de base : wood, stone, meat
- Salles de base : corridor, monster_room, trap_room, treasure_room, boss_room

## Stack
- Backend : FastAPI
- Frontend : HTML / CSS / JavaScript
- Sauvegarde : JSON local
- LLM : couche narrative seulement

## Installation
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

## Lancement
- API docs : `http://127.0.0.1:8000/docs`
- Front : ouvrir `frontend/index.html`
- Option simple : servir le front avec un petit serveur local

Exemple :
```bash
cd frontend
python -m http.server 8080
```

## Structure
Chaque dossier contient son propre `README.md` pour détailler son rôle.

## Convention de commits
Format recommandé :
```text
type(scope): summary
```

Exemples :
- `chore(repo): initialize project structure and docs`
- `feat(grid): add 10x10 dungeon placement`
- `feat(raid): add basic day-phase simulation`
- `feat(llm): add daily summary generator`

## Séquence de commits suggérée
1. `chore(repo): initialize project skeleton and base docs`
2. `feat(core): add initial models and constants`
3. `feat(grid): implement room placement rules`
4. `feat(pathfinding): add connected room traversal`
5. `feat(combat): add room combat and trap resolution`
6. `feat(economy): add resource generation and upkeep`
7. `feat(raid): add day-phase raid flow`
8. `feat(api): expose game and raid endpoints`
9. `feat(frontend): add prototype UI`
10. `feat(llm): add narrative services`
11. `test(core): add baseline tests`
12. `docs(game): extend design and roadmap`

## Summary de PR conseillé
```md
## Summary
This update introduces the initial playable foundations:
- 10x10 dungeon grid
- boss room placement rules
- day/night turn cycle
- basic hero raid simulation
- modular project documentation

## Why
This creates a stable MVP foundation for a dungeon management prototype with future LLM-driven narrative systems.

## Notes
- game balance values are placeholders
- LLM is not part of the source of truth
- saves are JSON-based for quick prototyping
```
