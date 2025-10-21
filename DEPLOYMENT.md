# CitizenAI Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Deploy to Render (Recommended)

**Steps:**

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to [https://render.com](https://render.com)
   - Sign up/Login with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** citizenai
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
   - Add Environment Variables:
     - `IBM_API_KEY` = your_api_key
     - `IBM_PROJECT_ID` = your_project_id
     - `IBM_URL` = https://us-south.ml.cloud.ibm.com
     - `FLASK_SECRET_KEY` = random_secret_key
   - Click "Create Web Service"

**✅ Done! Your app will be live in 5-10 minutes.**

---

### Option 2: Deploy to PythonAnywhere

**Steps:**

1. **Sign up:**
   - Go to [https://www.pythonanywhere.com](https://www.pythonanywhere.com)
   - Create a free account

2. **Upload your code:**
   - Go to "Files" tab
   - Upload all your project files
   - Or use Git to clone your repository

3. **Setup Virtual Environment:**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 citizenai
   pip install -r requirements.txt
   ```

4. **Configure Web App:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration" → Python 3.10
   - Set source code directory to your project folder
   - Edit WSGI configuration file:
     ```python
     import sys
     path = '/home/YOUR_USERNAME/CitizenAI'
     if path not in sys.path:
         sys.path.append(path)
     
     from app import app as application
     ```

5. **Set Environment Variables:**
   - In "Web" tab, scroll to "Environment variables"
   - Add your IBM credentials and Flask secret key

6. **Reload the web app**

**✅ Your app will be live at: YOUR_USERNAME.pythonanywhere.com**

---

### Option 3: Deploy to Railway

**Steps:**

1. **Push code to GitHub** (same as Render)

2. **Deploy on Railway:**
   - Go to [https://railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python
   - Add environment variables in Settings
   - Deploy!

**✅ Your app will auto-deploy with a generated URL.**

---

## 🔐 Important: Environment Variables

**Never commit these to GitHub!**

Set these in your deployment platform:

```
IBM_API_KEY=7yxZseSVHBJp8x0W2LvVqFU7IHBK2dHvhqBqHnPWvR_q
IBM_PROJECT_ID=c403c5dc-ecb4-4ffb-bf4e-97e6a6c1aa6c
IBM_URL=https://us-south.ml.cloud.ibm.com
FLASK_SECRET_KEY=create_a_random_secret_key_here
```

---

## 📝 Troubleshooting

**Issue:** App crashes on startup
- **Solution:** Check logs for missing dependencies, install all packages from requirements.txt

**Issue:** IBM AI not responding
- **Solution:** Verify environment variables are set correctly

**Issue:** Static files not loading
- **Solution:** Ensure static/ and templates/ folders are included in deployment

---

## 🎉 Post-Deployment

After deployment:
1. Test all pages: Home, Chat, Feedback
2. Verify AI chatbot responses
3. Test FormSpree feedback form
4. Check mobile responsiveness

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- PythonAnywhere Help: https://help.pythonanywhere.com
- Railway Docs: https://docs.railway.app
