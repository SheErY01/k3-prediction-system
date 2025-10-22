# K3 Prediction System

⚠️ **Important:** This repository contains a template project. Do NOT commit real credentials. Use environment variables or your hosting provider's secret storage.

## Structure
- `app/` - core modules (flask, prediction, email, scheduler)
- `main.py` - entrypoint (starts Flask + scheduler)
- `.env` - placeholders for environment variables
- `requirements.txt` - pip dependencies

## Setup (local)
1. Create a virtualenv and activate it.
2. Install dependencies: `pip install -r requirements.txt`
3. Fill environment variables (locally or in your host):
   - `GMAIL_USER`
   - `GMAIL_APP_PASSWORD`
   - `RECIPIENT_EMAIL`
   - `PORT` (optional)
4. Run: `python main.py`

## Deploy
- For Render: push repo to GitHub, create a Web Service, and set Environment Variables in the Render dashboard.
