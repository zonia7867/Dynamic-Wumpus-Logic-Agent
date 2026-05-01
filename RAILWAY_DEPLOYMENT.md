# RAILWAY_DEPLOYMENT.md

## Deploy Flask Backend to Railway (Step-by-Step)

Railway is the easiest way to deploy the Flask backend. It's **free** and handles everything for you.

---

## Prerequisites

- GitHub account
- Code pushed to GitHub repository
- Railway account (free: https://railway.app)

---

## Step-by-Step Railway Deployment

### 1. Login to Railway

1. Go to https://railway.app
2. Click "Login" → Sign in with GitHub
3. Authorize Railway to access your GitHub

### 2. Create New Project

1. Click "New Project"
2. Click "Deploy from GitHub repo"

### 3. Select Your Repository

1. Find "Wumpus agent" repository
2. Select it
3. Authorize if needed

### 4. Configure Project

Railway will automatically detect Python. If not:

1. Set Root Directory: `.` (root)
2. Railway should auto-detect `requirements.txt`

### 5. Deploy

1. Click "Deploy"
2. Wait for deployment to complete (2-3 minutes)

### 6. Get Your Backend URL

Once deployed:

1. Go to "Settings" tab
2. Find "Environment" section
3. Look for a URL like: `https://wumpus-backend-prod-*.railway.app`
4. Copy this URL

---

## Enable CORS (If Issues)

If frontend can't reach backend, update `backend/app.py`:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")  # Allow all origins
```

Then redeploy on Railway.

---

## Set Environment Variables (Optional)

If you need to configure anything:

1. In Railway dashboard, go to "Settings"
2. Click "Environment"
3. Add variables as needed

Most deployments work without this.

---

## Testing Deployed Backend

### Test with curl:

```bash
curl -X GET https://your-railway-url/api/status
```

Should return: `{"initialized": false}`

### Test with frontend:

1. Go to `frontend/config.html`
2. Enter your Railway URL: `https://your-railway-backend.railway.app`
3. Click "Go to Game"
4. Initialize a game

If it works, you're done! 🎉

---

## Common Issues

### "Cannot GET /api/status"

**Solution**: Make sure `app.py` has the `/api/` route. It should have:

```python
@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'Wumpus Agent Server is running!'})
```

### "CORS error in browser"

**Solution**: Add this to `app.py`:

```python
from flask_cors import CORS
CORS(app, origins="*", allow_headers="*", methods="*")
```

### "Build failed" on Railway

**Solution**: 
1. Check `requirements.txt` exists in `backend/` folder
2. All dependencies are listed:
   - Flask==2.3.0
   - Flask-CORS==4.0.0
3. Redeploy

---

## Redeploy After Changes

To redeploy after code changes:

1. Push code to GitHub
2. Railway auto-deploys from `main` branch
3. Check deployment status in Railway dashboard

---

## Logs & Debugging

### View logs:

1. In Railway dashboard
2. Click "Deployments"
3. Click latest deployment
4. See real-time logs

### Check if Flask is running:

Open your Railway URL in browser: `https://your-url/`

Should see: `{"status": "Wumpus Agent Server is running!"}`

---

## Cost

Railway provides:
- **Free tier**: 5GB/month + $5 credit
- **Perfect for**: This Wumpus Agent backend
- **Pricing**: Only pay if you exceed free tier

Total cost: **$0** for this project ✅

---

## Next Step

Once you have your Railway backend URL:

1. Go to `frontend/config.html`
2. Save your backend URL
3. You're connected! 🚀

---

## More Help

- Railway Docs: https://docs.railway.app
- Flask Docs: https://flask.palletsprojects.com
- Contact Railway support if issues

Happy deploying! 🎮
