# Copilot instructions for Shopina

## Architecture overview

- Two main projects: React/Vite frontend in [code source/front](code%20source/front) and Django REST backend in [code source/shopina-env/backend](code%20source/shopina-env/backend).
- Frontend → backend data flow: UI code calls centralized fetch helpers in [code source/front/src/services/api.ts](code%20source/front/src/services/api.ts), which hit Django REST endpoints under `/api/...`.
- Backend follows a clean architecture chain: Views → Serializers (DTOs) → Service Layer (business logic) → Repository Layer (data access) → Models. See [code source/shopina-env/backend/core](code%20source/shopina-env/backend/core) and the app folders in [code source/shopina-env/backend](code%20source/shopina-env/backend).

## Critical workflows (local dev)

- One-command Windows setup: [quick_setup.bat](quick_setup.bat) or [quick_setup.ps1](quick_setup.ps1) (creates venv, installs deps, runs servers).
- Backend dev server: run `manage.py runserver` from [code source/shopina-env/backend](code%20source/shopina-env/backend).
- Frontend dev server: `npm run dev` from [code source/front](code%20source/front). Port 3000 is enforced in [code source/front/vite.config.ts](code%20source/front/vite.config.ts).
- E2E tests: Playwright config is in [playwright.config.ts](playwright.config.ts). Use `npm run test:e2e` and install browsers with `npm run test:e2e:install`. Set `PLAYWRIGHT_NO_WEBSERVER=1` to reuse a running dev server and `E2E_REAL=1` to hit a real backend.

## Project-specific conventions

- API base URL is derived from `VITE_API_BASE` in [code source/front/src/utils/apiBase.ts](code%20source/front/src/utils/apiBase.ts) with a localhost fallback; keep this env var consistent when wiring new endpoints.
- Auth tokens are stored in `localStorage` and attached by `getAuthHeaders()` in [code source/front/src/services/api.ts](code%20source/front/src/services/api.ts); new API calls should reuse `handleResponse()` to handle Django HTML error pages safely.
- Backend feature work should follow the same layering: define model → repository → service → serializer → view → url entry, matching existing apps like `users`, `shop`, `orders`, `carts`, `payments`.

## Integration points

- Stripe: frontend uses `@stripe/react-stripe-js` and `@stripe/stripe-js` (see [code source/front/package.json](code%20source/front/package.json)); backend payment endpoints live in the `payments` app in [code source/shopina-env/backend](code%20source/shopina-env/backend).
- API docs are exposed via Swagger/ReDoc when the backend is running (documented in [code source/shopina-env/backend/README.md](code%20source/shopina-env/backend/README.md)).
