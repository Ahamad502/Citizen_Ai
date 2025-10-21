# 🚀 SETUP INSTRUCTIONS FOR CitizenAI

## ⚡ IMPORTANT - Read This First!

Your application has been **completely simplified** to include only:

1. **Home Page** (`/`) - Latest news + AI chatbot
2. **Feedback Page** (`/feedback`) - Form to submit feedback/complaints

All unnecessary code, pages, and files have been **REMOVED**.

---

## 📋 STEP-BY-STEP SETUP

### STEP 1: Install Python Packages

Open your terminal and run:

```bash
cd "c:\Users\ahama\Downloads\Citizen\CitizenAI"
pip install -r requirements.txt
```

### STEP 2: Configure IBM Watsonx AI

Your `.env` file already exists. Edit it with your IBM credentials:

1. Go to [https://cloud.ibm.com](https://cloud.ibm.com)
2. Sign in or create an account
3. Create a Watsonx.ai instance
4. Get your **API Key** and **Project ID**
5. Open `.env` file and add your credentials:

```env
IBM_API_KEY=your_actual_api_key_here
IBM_PROJECT_ID=your_actual_project_id_here
```

### STEP 3: Setup FormSpree (For Feedback Form)

This sends feedback directly to YOUR EMAIL:

1. Go to [https://formspree.io](https://formspree.io)
2. Click **"Sign Up"** (it's FREE)
3. Create a new account with your email
4. Click **"New Form"**
5. Copy your Form ID (looks like: `xyzabc123`)
6. Open `templates/feedback.html` in a text editor
7. Find this line (around line 118):
   ```html
   <form action="https://formspree.io/f/YOUR_FORMSPREE_ID" method="POST">
   ```
8. Replace `YOUR_FORMSPREE_ID` with your actual ID:
   ```html
   <form action="https://formspree.io/f/xyzabc123" method="POST">
   ```
9. Save the file

### STEP 4: Run Your Application

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### STEP 5: Open in Browser

Visit: **http://127.0.0.1:5000**

---

## 🎨 CUSTOMIZATION GUIDE

### Update News Items

1. Open `templates/index.html`
2. Find the news cards section (around line 290)
3. Edit or add new news cards:

```html
<div class="news-card">
  <h3>Your News Title</h3>
  <div class="date">Today's Date</div>
  <p>Your news content goes here...</p>
  <span class="tag">Category</span>
</div>
```

### Change Colors

To change the purple gradient to different colors:

1. Open `templates/index.html` or `templates/feedback.html`
2. Find this in the `<style>` section:
   ```css
   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
   ```
3. Replace with your colors (use [coolors.co](https://coolors.co) to find colors)

Example - Blue gradient:
```css
background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%);
```

---

## 🧪 TESTING

### Test the Chatbot:

1. Go to home page
2. Type a message in the chat box
3. Click "Send"
4. You should get a response from the AI

**Note:** If IBM Watsonx AI is not configured, you'll get a fallback message.

### Test the Feedback Form:

1. Click "Submit Feedback" button
2. Fill out the form
3. Click "Submit Feedback"
4. Check your email (the one registered with FormSpree)

---

## ❌ FILES REMOVED (You Don't Need These Anymore)

These files have been **DELETED**:

- `model.py` - No longer needed
- `chat_client.py` - Removed
- `chat_test.html` - Removed
- `debug_openai.py` - Removed
- `minimal_app.py` - Removed
- `server.js` - Removed
- All test files (`test_*.py`)
- Templates: `about.html`, `base.html`, `chat.html`, `dashboard.html`, `login.html`, `services.html`
- `__pycache__/` folder
- `flask_session/` folder

---

## 🆘 TROUBLESHOOTING

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: Chatbot responds with error message

**Solution:**
- Check your `.env` file has valid IBM credentials
- Make sure IBM_API_KEY and IBM_PROJECT_ID are correct
- Verify you have internet connection

### Problem: Feedback form doesn't send email

**Solution:**
- Verify FormSpree ID is correct in `templates/feedback.html`
- Check you verified your email with FormSpree
- Make sure the form action URL is: `https://formspree.io/f/YOUR_ID`

### Problem: Port 5000 already in use

**Solution:**
Edit `app.py`, change the last line:
```python
if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Use port 5001 instead
```

Then visit: `http://127.0.0.1:5001`

---

## 📱 WHAT EACH FILE DOES

```
CitizenAI/
├── app.py                   # Main Flask app (backend)
├── requirements.txt         # Python packages needed
├── .env                     # Your secret credentials (DO NOT SHARE)
├── .env.example            # Template for .env
├── README.md               # Main documentation
├── SETUP.md                # This file
├── templates/
│   ├── index.html         # Home page (news + chat)
│   └── feedback.html      # Feedback form page
└── static/                 # For images/CSS (currently empty)
```

---

## ✅ FINAL CHECKLIST

Before going live:

- [ ] Installed all packages (`pip install -r requirements.txt`)
- [ ] Added IBM Watsonx AI credentials to `.env`
- [ ] Setup FormSpree and updated `feedback.html`
- [ ] Tested chatbot (sends and receives messages)
- [ ] Tested feedback form (receives email)
- [ ] Updated news content in `index.html`
- [ ] Customized colors/branding (optional)
- [ ] Changed `FLASK_SECRET_KEY` in `.env` to something random

---

## 🎯 NEXT STEPS

1. **Run the app:** `python app.py`
2. **Test everything:** Chat, feedback form, navigation
3. **Customize:** Update news, change colors, add your branding
4. **Deploy:** (Optional) Deploy to Heroku, PythonAnywhere, or other hosting

---

## 💪 YOU GOT THIS!

Your app is now **super clean** and **focused**. No more complexity, just:
- One home page with news and chat
- One feedback page
- Clean, simple code

**Need help?** Check the README.md or the troubleshooting section above.

---

**Good luck! 🚀**
