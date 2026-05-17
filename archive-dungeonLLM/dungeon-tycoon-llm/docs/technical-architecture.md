# Technical Architecture

## Backend
FastAPI expose l'état de jeu, le placement des salles, la simulation et les appels narratifs.

## Frontend
Interface légère en HTML/CSS/JS :
- rendu de grille
- palette de salles
- panneaux état / ressources / logs

## Source of truth
La logique métier reste déterministe dans le backend.
Le LLM n'est utilisé que pour :
- narration
- flavor text
- résumés de journée
- traits textuels de héros

## Data
Les données statiques sont stockées en JSON dans `backend/app/data/`.
Les sauvegardes locales sont stockées dans `saves/`.
