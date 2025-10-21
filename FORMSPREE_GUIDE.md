# 📧 FormSpree Setup Guide - Get Feedback to Your Email

## What is FormSpree?

FormSpree is a FREE service that sends form submissions directly to your email.
No backend code needed! Perfect for your feedback form.

---

## 🚀 Step-by-Step Setup (5 Minutes)

### Step 1: Sign Up

1. Go to: **https://formspree.io**
2. Click **"Get Started"** or **"Sign Up"**
3. Enter your email address
4. Create a password
5. Click **"Create Account"**

### Step 2: Verify Email

1. Check your email inbox
2. Click the verification link from FormSpree
3. You're now verified! ✅

### Step 3: Create a Form

1. Login to FormSpree dashboard
2. Click **"+ New Form"**
3. Give it a name: "CitizenAI Feedback"
4. Click **"Create Form"**

### Step 4: Get Your Form ID

After creating the form, you'll see:

```
Form Endpoint: https://formspree.io/f/xyzabc123
                                        ^^^^^^^^
                                     This is your ID!
```

Copy this ID (example: `xyzabc123`)

### Step 5: Update Your Code

1. Open: `templates/feedback.html`
2. Find line 118 (or search for "YOUR_FORMSPREE_ID")
3. You'll see:
   ```html
   <form action="https://formspree.io/f/YOUR_FORMSPREE_ID" method="POST">
   ```
4. Replace `YOUR_FORMSPREE_ID` with your actual ID:
   ```html
   <form action="https://formspree.io/f/xyzabc123" method="POST">
   ```
5. Save the file

### Step 6: Test It!

1. Run your app: `python app.py`
2. Go to: `http://127.0.0.1:5000/feedback`
3. Fill out the form
4. Click "Submit Feedback"
5. Check your email! 📬

---

## ✨ FormSpree Free Plan Features

- ✅ 50 submissions per month
- ✅ Email notifications
- ✅ Spam filtering
- ✅ File uploads
- ✅ Email confirmation to submitter

**More than enough for most projects!**

---

## 🎯 What You'll Receive in Email

Each feedback submission will include:

```
From: FormSpree <noreply@formspree.io>
Subject: New submission from CitizenAI Feedback

Name: John Doe
Email: john@example.com
Phone: +1 (555) 123-4567
Submission Type: Complaint
Subject: Issue with community park
Message: The playground equipment needs maintenance...
```

---

## 🔧 Advanced Settings (Optional)

In your FormSpree dashboard, you can:

1. **Custom Redirect** - Redirect after form submission
2. **Auto-reply** - Send confirmation email to user
3. **Webhooks** - Send data to other services
4. **Spam Protection** - Block spam submissions
5. **Export Data** - Download all submissions as CSV

---

## ⚠️ Important Notes

- **Keep your Form ID private** - Don't share it publicly
- **Free plan limit** - 50 submissions/month (upgrade if needed)
- **Email delivery** - Check spam folder if not receiving
- **Form must be on live domain** - Local testing works, but verify email

---

## 🆘 Troubleshooting

### Not receiving emails?

1. Check spam/junk folder
2. Verify your email in FormSpree dashboard
3. Test with FormSpree's test page first
4. Check FormSpree dashboard for submissions

### Form not submitting?

1. Verify Form ID is correct (no typos)
2. Check internet connection
3. Look at browser console for errors (F12)
4. Verify form action URL format

### "Form not found" error?

- Your Form ID is incorrect
- Double-check: `https://formspree.io/f/YOUR_ID`
- Make sure form is active in dashboard

---

## 📱 FormSpree Dashboard Overview

After setup, your dashboard shows:

```
┌─────────────────────────────────────┐
│  CitizenAI Feedback                 │
│  ───────────────────                │
│  📊 Submissions: 5                  │
│  📧 Email: your@email.com           │
│  🔗 Endpoint: formspree.io/f/xyz123 │
│                                     │
│  [View Submissions] [Settings]      │
└─────────────────────────────────────┘
```

Click "View Submissions" to see all feedback received.

---

## 🎉 You're Done!

Your feedback form now sends directly to your email.

**No server-side code. No database. Just works!**

---

## 💡 Pro Tips

1. **Bookmark FormSpree dashboard** - Easy access to submissions
2. **Set up email filters** - Auto-label feedback emails
3. **Check weekly** - Stay on top of feedback
4. **Respond quickly** - Build trust with users
5. **Export data** - Keep records of feedback

---

## 🔗 Useful Links

- FormSpree: https://formspree.io
- Documentation: https://help.formspree.io
- Pricing: https://formspree.io/pricing
- Support: help@formspree.io

---

**That's it! Your feedback form is ready to receive submissions! 🚀**
