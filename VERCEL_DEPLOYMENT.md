# VERCEL_DEPLOYMENT.md

## Deploy Frontend to Vercel (Step-by-Step)

Vercel makes it incredibly easy to deploy static sites. **Free tier includes unlimited deployments!**

---

## Prerequisites

- GitHub account
- Code pushed to GitHub repository
- Vercel account (free: https://vercel.com)
- Your deployed backend URL (from Railway)

---

## Step-by-Step Vercel Deployment

### 1. Login to Vercel

1. Go to https://vercel.com
2. Click "Sign Up" → Choose "Continue with GitHub"
3. Authorize Vercel to access GitHub

### 2. Create New Project

1. Go to Vercel dashboard
2. Click "Add New..." → "Project"
3. Click "Import Git Repository"

### 3. Select Repository

1. Find "Wumpus agent" repository
2. Click "Import"

### 4. Configure Project

1. **Project Name**: Keep default or change to "wumpus-agent"
2. **Root Directory**: Click "Edit" → Select `frontend`
3. **Build Command**: Leave empty (static site)
4. **Output Directory**: Leave empty
5. **Environment Variables**: 
   - Name: `VITE_API_URL`
   - Value: `https://your-railway-backend.railway.app` (without `/api`)

### 5. Deploy

Click "Deploy"

Wait 1-2 minutes for deployment to complete.

### 6. Get Your Frontend URL

Once deployed:

1. Vercel shows your production URL
2. Example: `https://wumpus-agent.vercel.app`
3. Click on it to open your deployed game!

---

## Complete Setup Checklist

- [ ] Backend deployed to Railway (got URL)
- [ ] Frontend imported into Vercel
- [ ] Root directory set to `frontend`
- [ ] Environment variable `VITE_API_URL` added
- [ ] Deploy completed successfully
- [ ] Can access website: `https://your-project.vercel.app`

---

## Update Backend URL (If Changed)

If you need to change your backend URL:

1. Go to Vercel project settings
2. Click "Environment Variables"
3. Edit `VITE_API_URL` value
4. Redeploy by clicking "Deployments" → "Redeploy"

---

## Testing Deployed Site

1. Open your Vercel URL in browser
2. Click "Configure Backend" link (if shown)
3. Or manually enter backend URL and save
4. Initialize a game
5. Auto-move should work

---

## Automatic Deployments

After first deployment:

1. **Every GitHub push** to `main` branch = auto-deploy
2. No manual action needed
3. Check deployment status on Vercel dashboard
4. Previous deployments stay live (can rollback)

---

## Custom Domain (Optional)

To use your own domain:

1. In Vercel project settings
2. Click "Domains"
3. Add your domain
4. Follow DNS configuration steps
5. Done! 🎉

---

## Common Issues

### "Cannot find root directory"

**Solution**: 
1. Go to project settings
2. Click "Root Directory"
3. Select `frontend`
4. Redeploy

### "Blank page or 404"

**Solution**:
1. Check root directory is `frontend`
2. Make sure `index.html` exists in frontend folder
3. Check browser console (F12) for errors

### "API connection failed"

**Solution**:
1. Check `VITE_API_URL` is set correctly
2. Backend URL must NOT have `/api` at end
3. Go to `config.html` page to update URL
4. Test backend URL directly in browser

---

## Troubleshooting

### Check Vercel Logs

1. Go to Vercel dashboard
2. Click project name
3. Go to "Deployments" tab
4. Click latest deployment
5. See build logs

### Test Frontend Locally

Before deploying, test locally:

```bash
cd frontend
python -m http.server 8000
# Open: http://localhost:8000
```

---

## Cost

Vercel free tier includes:
- ✅ Unlimited deployments
- ✅ Unlimited bandwidth
- ✅ Automatic HTTPS
- ✅ Custom domains
- ✅ Collaboration

**Perfect for this project. Cost: $0** ✅

---

## Production Tips

1. **Set a descriptive project name**: Makes it easier to find
2. **Add README**: Go to Vercel dashboard, add project description
3. **Monitor analytics**: Check deployment analytics in Vercel dashboard
4. **Setup notifications**: Get notified of failed deployments

---

## Next Steps After Deployment

1. ✅ Share your frontend URL: `https://your-project.vercel.app`
2. ✅ Test with friends/family
3. ✅ Celebrate! 🎉

---

## More Help

- Vercel Docs: https://vercel.com/docs
- GitHub Integration: https://vercel.com/docs/git
- Environment Variables: https://vercel.com/docs/concepts/projects/environment-variables

Enjoy your live Wumpus Agent game! 🚀🎮
