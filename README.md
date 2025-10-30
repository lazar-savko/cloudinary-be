
# Backend (Flask + SQLite + Cloudinary)

Minimal API to:

* **GET** `/ping` – health check
* **POST** `/media/signature` – returns signed params for direct Cloudinary upload
* **POST** `/users/me/avatar` – saves **only the Cloudinary `secure_url`** to SQLite

## 1) Prereqs

* Python 3.10+
* Cloudinary account (cloud name, API key, API secret)

## 2) Install

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

## 3) Configure

Create `.env` in `backend/`:

```
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
CLOUDINARY_CLOUD_NAME=your_cloud
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret
```

> We’re using **signed upload without a preset**. (You can add one later if you want Cloudinary to enforce file size/formats.)

## 4) Run

```bash
python app.py
# Server on http://localhost:5000
```

## 5) Endpoints (quick)

* `POST /media/signature`
  Body:

  ```json
  { "user_id": "1" }
  ```

  Response includes: `cloud_name, api_key, signature, timestamp, folder, public_id, overwrite`.

* `POST /users/me/avatar`
  Body:

  ```json
  { "user_id": 1, "secure_url": "https://res.cloudinary.com/.../avatar.jpg" }
  ```

  Saves link to the demo user.

* `GET /ping` → `{ "ok": true }`

## 6) Dev tips

* Run from the `backend/` folder so imports work.
* Frontend dev server should proxy `/media` and `/users` to `http://localhost:5000`.

---
