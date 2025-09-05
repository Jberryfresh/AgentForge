# AgentForge (Starter Monorepo)

Scaffold for multi-agent orchestration.

## Backend (orchestrator) environment

- Recommended Python: 3.12 (PyO3/pydantic-core does not yet fully support 3.13)
- Create venv and install:

```
python3.12 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r services/orchestrator/requirements.txt
```

- Run locally:

```
uvicorn services.orchestrator.app.main:app --reload
```

- A2A WebSocket demo (in separate terminals):

```
python services/orchestrator/examples/agent_b.py
python services/orchestrator/examples/agent_a.py
```

If you use Python 3.13, installing pydantic-core may fail due to PyO3 constraints; use Python 3.12.

## Frontend (apps/web)

A minimal Next.js 14 app with TypeScript and ESLint lives in `apps/web`. It includes a simple status widget that pings your backend's `/health` endpoint.

### Run locally

- Prerequisites: Node.js 18+ and npm
- Configure the API base URL (optional): copy `apps/web/.env.example` to `apps/web/.env` and adjust `NEXT_PUBLIC_API_URL` if your backend is not on `http://localhost:8000`.

```
cd apps/web
npm install
npm run dev
```

Open `http://localhost:3000` in your browser. When your backend is running and serving `GET /health`, the page will show `Backend status: online`.

### Linting

```
cd apps/web
npm run lint
```

### Build and start

```
cd apps/web
npm run build
npm start
```
