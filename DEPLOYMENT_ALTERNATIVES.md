# Alternative Deployment Options (Windows PowerShell Issues)

Since Railway CLI has PowerShell execution policy issues on Windows, here are better alternatives:

## Option 1: Render (Recommended - No CLI needed)

1. **Go to https://render.com**
2. **Sign up/Login with GitHub**
3. **Create New Web Service:**
   - Connect your GitHub repository
   - Root Directory: `db`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
   - Python Version: 3.11

4. **Add PostgreSQL Database:**
   - Create New PostgreSQL database
   - Copy the DATABASE_URL

5. **Set Environment Variables:**
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key-here`
   - `DATABASE_URL=postgresql://...` (from step 4)

6. **Deploy!** Render will automatically build and deploy

## Option 2: Heroku (Web Interface)

1. **Go to https://heroku.com**
2. **Create New App**
3. **Connect GitHub repository**
4. **Add PostgreSQL addon:**
   - Resources tab → Add-ons → Heroku Postgres
5. **Set Config Vars:**
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key`
6. **Deploy from GitHub**

## Option 3: Railway (Fix PowerShell first)

If you want to use Railway, fix PowerShell first:

```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then:
```bash
npm install -g @railway/cli
railway login
railway init
railway add postgresql
railway deploy
```

## Option 4: Local Development (Current)

Your backend is running locally on http://localhost:5050

**Test it:**
- Health check: http://localhost:5050/health
- Your website form will submit to: http://localhost:5050/api/leads

## Update Frontend for Production

Once you deploy, update your website:

1. **Create `.env` in website folder:**
   ```
   VITE_BACKEND_URL=https://your-app-name.onrender.com
   ```

2. **Or update `website/src/utils/formSubmission.js`:**
   ```javascript
   const API_URL = 'https://your-app-name.onrender.com';
   ```

## Quick Test Commands

Test your local backend:
```bash
# Health check
curl http://localhost:5050/health

# Test lead submission
curl -X POST http://localhost:5050/api/leads \
  -H "Content-Type: application/json" \
  -d '{"firstName":"Test","lastName":"User","email":"test@example.com","phone":"555-1234","streetAddress":"123 Main St","city":"Charleston","state":"SC","zip":"29401","referrer":"Google","service":["exterior"]}'
```


