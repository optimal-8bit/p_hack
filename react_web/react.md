# Frontend Engineering Guide (React + Redux)

## Goal
Build fast, maintainable frontend features with minimal merge conflicts.

This project uses:
- React + Vite
- Redux Toolkit for state management
- React Router for route-level structure
- Central API client for backend communication
- Service layer per domain

## Core Principles
1. Keep UI components focused on rendering and user interaction.
2. Keep API and business calls out of components.
3. Use Redux async thunks for server-driven state changes.
4. Reuse central API client for all HTTP calls.
5. Keep features isolated by folder to reduce conflicts.

## Folder Conventions

### src/lib
Shared low-level utilities.

- `apiClient.js`
	- Single HTTP entrypoint.
	- Adds auth token automatically.
	- Handles error normalization.

- `authToken.js`
	- Token get/set/remove helpers.

### src/services
Domain service functions that call backend routes.

- `authService.js`
	- register
	- login
	- loginWithGoogle
	- me

- `chatService.js`
	- streamReply (streaming token response + file upload support)

Add one service file per backend module when building new features.

### src/features
Redux slices and state orchestration.

- `features/auth/authSlice.js`
	- async thunks
	- loading/error state
	- token/user updates

Rule: UI never calls `apiClient` directly when a service exists.

### src/pages
Route-level pages.

- `LoginPage.jsx`
- `RegisterPage.jsx`
- `DashboardPage.jsx`
- `ChatTemplatePage.jsx` (template only, not route-wired by default)

### src/components
Reusable UI and wrappers.

- `ProtectedRoute.jsx`

### src/routes
App route map and route guards.

- `AppRouter.jsx`

### src/app
App-level setup.

- `store.js`

## Data Flow Standard
Use this flow for all new features:

1. Page/component dispatches Redux thunk.
2. Thunk calls service function.
3. Service calls central API client.
4. API client performs request and handles errors.
5. Thunk updates Redux state.
6. UI re-renders from Redux state.

This gives one consistent call path across the app.

## API Client Rules
1. Put base URL only in env: `VITE_API_BASE_URL`.
2. Put token attachment logic only in `apiClient`.
3. Normalize error messages in one place.
4. Keep HTTP method wrappers (`get/post/put/del`) consistent.

Never hardcode backend URLs in components.

## Service Layer Rules
1. One service file per feature/domain.
2. Service methods should map clearly to backend routes.
3. Return raw backend payload, do not mutate heavily in service.
4. Keep service functions small and predictable.

Example pattern:
- `itemsService.list()` -> `GET /items`
- `itemsService.create(payload)` -> `POST /items`
- `chatService.streamReply(payload)` -> streaming backend endpoint

## Chat Template Notes
1. Chat template UI is in `src/pages/ChatTemplatePage.jsx`.
2. It supports:
	 - markdown rendering for assistant output
	 - backend token streaming
	 - multi-file attachment upload
	 - user stop generation control
3. It is intentionally not route-wired so it can be mounted where needed.
4. Streaming parser supports SSE-style `data:` lines and plain chunk text.
5. Keep all chat network handling inside `chatService` + `apiClient.stream`.

## Redux Slice Rules
1. Use `createAsyncThunk` for async backend operations.
2. Keep `status` and `error` in state for UI feedback.
3. Use slice reducers for local events (clear error, logout, reset form state).
4. Keep side effects in thunk logic, not in components.

## Route Guard Rules
1. Any protected page must be wrapped in `ProtectedRoute`.
2. Redirect unauthenticated users to `/login`.
3. Keep auth checks token-driven and simple.

## Google OAuth Notes
1. Use `@react-oauth/google` provider in app root.
2. Put Google client id in env: `VITE_GOOGLE_CLIENT_ID`.
3. Send credential token to backend route `/auth/google` through service layer.

## Naming Conventions
1. `FeaturePage.jsx` for routes.
2. `featureService.js` for API wrappers.
3. `featureSlice.js` for Redux state.
4. Thunk names should be action-like:
	 - `loginUser`
	 - `registerUser`
	 - `fetchCurrentUser`

## Styling Rules
1. Keep shared primitives in `index.css`.
2. Keep app/page-level styles in `App.css` unless component-level styles are needed.
3. Avoid inline styles except tiny one-offs.

## Fast Team Workflow
1. Build by feature folders to reduce merge conflicts.
2. Touch shared files (`store.js`, `AppRouter.jsx`) only when required.
3. Open small PRs by module (auth, items, rag UI, etc).
4. Keep each PR scoped to one feature path.

## Checklist for New Feature
1. Add service functions in `src/services`.
2. Add slice and thunks in `src/features/<feature>`.
3. Add page and route if needed.
4. Connect UI with `useDispatch` + `useSelector`.
5. Handle loading, success, and error states.
6. Keep backend URL and token handling only in central client.

## Environment Variables
Use:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_GOOGLE_CLIENT_ID=
VITE_CHAT_STREAM_PATH=/chat/stream
```

## Non-Negotiables
1. No direct fetch calls inside pages when service exists.
2. No duplicated token logic outside `authToken` + `apiClient`.
3. No backend route strings scattered across components.
4. Keep architecture consistent over quick hacks.
