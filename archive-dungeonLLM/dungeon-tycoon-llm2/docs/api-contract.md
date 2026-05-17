# API Contract

## Endpoints MVP
- `GET /api/game/state`
- `POST /api/game/new`
- `POST /api/grid/place-room`
- `POST /api/grid/remove-room`
- `POST /api/turn/night/resolve`
- `POST /api/turn/day/start-raid`
- `GET /api/raid/{raid_id}`
- `POST /api/llm/daily-summary`

## Objectif
Conserver une séparation nette entre :
- état de jeu
- commandes de mutation
- résultat de simulation
- narration
