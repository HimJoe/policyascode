# Quick Push to GitHub Guide

## 🚀 3 Simple Steps to Deploy

### Step 1: Create Repository on GitHub
1. Go to https://github.com/HimJoe
2. Click **"New"** repository button
3. Repository name: `policy-as-code`
4. **DO NOT** check "Initialize with README"
5. Click **"Create repository"**

### Step 2: Run These Commands

Open Terminal and run:

```bash
# Navigate to project
cd "/Users/himanshujoshi/Downloads/Policiy as a code"

# Add GitHub remote (use YOUR actual repository URL from GitHub)
git remote add origin https://github.com/HimJoe/policy-as-code.git

# Rename branch to main (recommended)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 3: Verify
Go to https://github.com/HimJoe/policy-as-code and see your code!

---

## 🎯 Complete Command Sequence

```bash
cd "/Users/himanshujoshi/Downloads/Policiy as a code"
git remote add origin https://github.com/HimJoe/policy-as-code.git
git branch -M main
git push -u origin main
```

That's it! Your Policy-as-Code app is now on GitHub! 🎉

---

## 📝 Repository Details

**Repository URL**: https://github.com/HimJoe/policy-as-code
**Project Name**: GRC Multi-Agent Governance System
**Description**: Multi-agent AI system for automated GRC policy enforcement

---

## 🌐 Optional: Deploy to Streamlit Cloud

After pushing to GitHub:

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `HimJoe/policy-as-code`
5. Main file: `streamlit_app.py`
6. Click "Deploy"

Your app will be live at: `https://[name].streamlit.app`

---

## ⚠️ Troubleshooting

**If you get "authentication failed":**
1. Go to GitHub Settings → Developer settings → Personal Access Tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `workflow`
4. Use token as password when pushing

**If remote already exists:**
```bash
git remote remove origin
git remote add origin https://github.com/HimJoe/policy-as-code.git
git push -u origin main
```

---

## 📚 More Information

- Full setup guide: See `GITHUB_SETUP.md`
- Deployment guide: See `DEPLOYMENT.md`
- Contributing: See `CONTRIBUTING.md`
- Quick start: See `QUICKSTART.md`

---

**Need Help?** Read `GITHUB_SETUP.md` for detailed instructions!
