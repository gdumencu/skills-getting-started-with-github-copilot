# GitHub Copilot Instructions

This is a FastAPI-based web application for managing extracurricular activities at Mergington High School.

## Architecture Overview

**Tech Stack:**
- **Backend:** FastAPI (Python) with Uvicorn server
- **Frontend:** Vanilla JavaScript + HTML/CSS
- **Data Storage:** In-memory dictionary (resets on server restart)

**Key Components:**
- `src/app.py` - FastAPI application with two main endpoints
- `src/static/` - Frontend assets (HTML, CSS, JavaScript)
  - `index.html` - Two-section UI: activities list + signup form
  - `app.js` - Fetches activities, populates UI, handles signup
  - `styles.css` - Responsive styling

## Data Model & API Design

**Activities:** Identified by name (string), containing:
- `description`, `schedule`, `max_participants`, `participants` (list of emails)

**Key endpoints:**
- `GET /activities` - Returns all activities as JSON object
- `POST /activities/{activity_name}/signup?email={email}` - Adds student to activity

**Important patterns:**
- Activity names used as dict keys; maintain consistency when referencing activities
- Email validation happens client-side only; server accepts any string
- No capacity check enforced in signup endpoint (validation incomplete - see `app.py` line ~60)
- Redirect `GET /` to `/static/index.html` via `RedirectResponse`

## Developer Workflows

**Running the application:**
```bash
cd /workspaces/skills-getting-started-with-github-copilot
pip install -r requirements.txt
python src/app.py
```
Then open http://localhost:8000 in browser.

**Testing:**
```bash
pytest  # Uses pythonpath config from pytest.ini
```

**FastAPI auto-generated docs:** http://localhost:8000/docs (Swagger UI)

## Frontend Communication Pattern

The frontend (`app.js`) follows this flow:
1. On page load, fetch `/activities` to populate:
   - Activities cards (display view of all activities with participant counts)
   - Dropdown menu for signup form
2. On form submit, POST to `/activities/{name}/signup?email={email}`
3. Display success/error message in `#message` div, auto-hide after 5 seconds

**Critical detail:** Activity names in `encodeURIComponent()` calls to handle spaces (e.g., "Chess Club" → "Chess%20Club")

## Project-Specific Conventions

- **Error handling:** Frontend catches fetch errors; server returns HTTPException with 404/400 status codes
- **Capacity limits:** Defined per activity but not enforced server-side (incomplete implementation)
- **Email format:** No validation; any string accepted
- **State persistence:** None—all data lost on server restart (design choice for this educational app)
- **HTML structure:** IDs used as hooks in JavaScript (`#activities-list`, `#signup-form`, etc.)—maintain naming when modifying templates

## When to Modify Each Component

- **Backend logic:** Modify `app.py` activities dict or endpoint handlers
- **UI updates:** Modify `app.js` (fetching/rendering) or `index.html` (structure) or `styles.css`
- **New features:** Consider if server-side validation (e.g., capacity enforcement) or client-side polish (e.g., form validation) is needed
