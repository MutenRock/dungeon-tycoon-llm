# Backend

Backend FastAPI du prototype.

## Rôle
- porter l'état de jeu
- appliquer les règles de gameplay
- exposer les endpoints API
- simuler les raids
- appeler éventuellement le service narratif LLM

## Lancement
```bash
uvicorn backend.app.main:app --reload
```

## Organisation
- `app/api/` : routes
- `app/core/` : boucle et règles
- `app/models/` : modèles métier
- `app/services/` : logique applicative
- `app/data/` : données statiques
- `tests/` : tests backend
