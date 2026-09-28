# Deployment: Vercel + Render

The visual/UI source files are unchanged. Deployment configuration has been added around the existing project.

## 1. Push this project to GitHub

Push the whole `AI-Usage-Analysis` folder to a GitHub repository.

## 2. Deploy the Flask backend on Render

In Render, create a **Web Service** from the GitHub repository.

- Root Directory: `backend`
- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

Render will give you a backend URL such as:
`https://your-backend-name.onrender.com`

Test it by opening:
`https://your-backend-name.onrender.com/api/health`

It should return JSON with `status: ok`.

## 3. Deploy the React frontend on Vercel

In Vercel, import the same GitHub repository.

- Root Directory: `frontend`
- Framework Preset: Vite
- Build Command: `npm run build`
- Output Directory: `dist`

Add an Environment Variable:

- Name: `VITE_API_URL`
- Value: your Render backend URL, for example `https://your-backend-name.onrender.com`

Redeploy after adding the variable.

## 4. Important SQLite note

This project keeps SQLite because it is a mini-project. SQLite is suitable for local/demo use, but a normal Render web service does not provide durable database storage across all restarts/redeploys. If the online version must permanently retain many students' responses, move the database to a hosted PostgreSQL service later.
