# WisdomWealth Agents - Railway Deployment

## Environment Variables

Set these in Railway dashboard:

```bash
GEMINI_API_KEY=AIzaSyCvJvE7DMeIURv9QN1Lck7xQgFXFa4L_6s
PORT=8000
HOST=0.0.0.0
DATA_DIR=/data
CHROMA_DIR=/data/chroma_db
ENABLE_RETRIEVAL=true
ENVIRONMENT=production
```

## Deployment Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Volume Mount

- Mount persistent volume at `/data` for SQLite and ChromaDB storage

## Health Check

- Path: `/health`
- Expected: 200 status with JSON response

## Public URL

After deployment, note the Railway public URL for frontend integration:
`https://your-app-name.railway.app`