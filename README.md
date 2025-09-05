# AgentForge (Starter Monorepo)

Scaffold for multi-agent orchestration.

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
