# Circadian Intelligence — Frontend

A standalone Nuxt 2 + Vue 2 frontend for the Circadian physiological intelligence backend.

## Quick Start

### 1. Install dependencies
```bash
npm install --legacy-peer-deps
```

### 2. Start (Windows)
Double-click `start.bat`  
OR in terminal:
```bash
set NODE_OPTIONS=--openssl-legacy-provider
npm run dev
```

### 3. Open browser
```
http://localhost:3000/circadian
```

Make sure your FastAPI backend is running on port 8000.

---

## Pages
- `/circadian` — Main dashboard
- `/circadian/timeline` — 24h biological clock
- `/circadian/interventions` — Active zeitgebers
- `/circadian/trends` — Trends & forecast
- `/circadian/notifications` — Alerts

## Environment
Edit `nuxt.config.js` to change the API URL or user ID:
```js
env: {
  CIRCADIAN_API_URL: 'http://localhost:8000',
  CIRCADIAN_USER_ID: '659f5c51-ca99-4f1b-85b9-9bc0185fff36'
}
```
