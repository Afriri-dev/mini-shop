# Routes Auth (work in progress)

**Point d'entrée actuel :** `app.py` à la racine de `src/`.

Les routes actives sont définies directement dans `app.py` :
- `POST /auth/signup` — Inscription (username, email, password)
- `POST /auth/login` — Connexion (email, password)
- `GET /auth/health` — Health check + connexion DB

Les Blueprints dans ce dossier (`login.py`, `register.py`, `health.py`) sont une version alternative en cours de développement. Ils ne sont **pas encore intégrés** dans `app.py`.

Pour une refactorisation future : consolider ces blueprints avec le préfixe `/auth/` et aligner le comportement (hash bcrypt, email pour login, etc.) sur `app.py`.
