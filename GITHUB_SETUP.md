# GitHub Setup Guide

This guide will help you push your GRC Multi-Agent Governance System to GitHub.

## Step 1: Create a New Repository on GitHub

1. Go to [GitHub](https://github.com/HimJoe)
2. Click the **"+"** icon in the top-right corner
3. Select **"New repository"**
4. Fill in the repository details:
   - **Repository name**: `policy-as-code` (or your preferred name)
   - **Description**: `GRC Multi-Agent Governance System - Policy-as-Code with automated compliance enforcement`
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

## Step 2: Connect Your Local Repository to GitHub

After creating the repository, GitHub will show you setup instructions. Follow these commands in your terminal:

```bash
# Navigate to your project directory
cd "/Users/himanshujoshi/Downloads/Policiy as a code"

# Add the remote repository (replace with your actual repository URL)
git remote add origin https://github.com/HimJoe/policy-as-code.git

# Rename branch to main (optional, recommended)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

## Step 3: Verify Your Repository

1. Go to your repository on GitHub: `https://github.com/HimJoe/policy-as-code`
2. You should see all your files and the README.md displayed
3. Check that the following are visible:
   - README.md with full documentation
   - All Python files (grc_agent_system.py, document_processor.py, streamlit_app.py)
   - requirements.txt
   - Dockerfile and docker-compose.yml
   - .github/workflows for CI/CD

## Step 4: Configure Repository Settings (Optional but Recommended)

### Add Topics
1. Go to your repository
2. Click the gear icon next to "About"
3. Add topics: `policy-as-code`, `grc`, `compliance`, `multi-agent`, `streamlit`, `governance`, `python`, `banking`, `fintech`, `ai-governance`

### Enable GitHub Pages (for documentation)
1. Go to Settings → Pages
2. Select branch: `main`
3. Select folder: `/docs` or `root`
4. Save

### Add Repository Description
Add this description in the "About" section:
```
Multi-agent AI system for automated GRC policy enforcement. Converts compliance policies into executable code with real-time validation for banking & finance.
```

### Add Website
If deploying to Streamlit Cloud or other hosting:
```
https://your-app.streamlit.app
```

## Step 5: Deploy to Streamlit Cloud (Optional)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select:
   - Repository: `HimJoe/policy-as-code`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
5. Click **"Deploy!"**
6. Your app will be live at: `https://[app-name].streamlit.app`

## Step 6: Set Up Branch Protection (Recommended for Production)

1. Go to Settings → Branches
2. Click "Add rule"
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
5. Save changes

## Step 7: Add Secrets for CI/CD (If needed later)

1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add any secrets needed for deployment:
   - `STREAMLIT_SHARING_TOKEN`
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - etc.

## Alternative: Using GitHub CLI (gh)

If you have GitHub CLI installed:

```bash
# Login to GitHub
gh auth login

# Create repository and push
gh repo create policy-as-code --public --source=. --remote=origin --push

# Open repository in browser
gh repo view --web
```

## Common Issues and Solutions

### Issue 1: Authentication Failed
**Solution**: Use a Personal Access Token instead of password
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`
4. Copy the token
5. Use token as password when pushing

### Issue 2: Remote Already Exists
**Solution**: Remove and re-add the remote
```bash
git remote remove origin
git remote add origin https://github.com/HimJoe/policy-as-code.git
git push -u origin main
```

### Issue 3: Branch Name Mismatch
**Solution**: Rename your branch
```bash
git branch -M main
git push -u origin main
```

### Issue 4: Large Files
**Solution**: Use Git LFS for large files
```bash
git lfs install
git lfs track "*.pdf"
git add .gitattributes
git commit -m "Add Git LFS tracking"
git push
```

## Quick Reference Commands

```bash
# Check remote status
git remote -v

# View commit history
git log --oneline --graph --all

# Check repository status
git status

# Pull latest changes
git pull origin main

# Push new changes
git add .
git commit -m "Your commit message"
git push origin main

# Create and switch to new branch
git checkout -b feature/new-feature

# Switch back to main
git checkout main

# Merge feature branch
git merge feature/new-feature
```

## Repository Structure

After pushing, your repository will have:

```
policy-as-code/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── workflows/
│       └── python-app.yml
├── .dockerignore
├── .gitignore
├── CONTRIBUTING.md
├── DEPLOYMENT.md
├── Dockerfile
├── GITHUB_SETUP.md
├── LICENSE
├── PROJECT_SUMMARY.md
├── QUICKSTART.md
├── README.md
├── architecture_diagram.mermaid
├── demo.py
├── docker-compose.yml
├── document_processor.py
├── grc_agent_system.py
├── requirements.txt
├── sample_banking_policy.txt
└── streamlit_app.py
```

## Next Steps After Pushing

1. ✅ Add repository description and topics
2. ✅ Create a release (v1.0.0)
3. ✅ Deploy to Streamlit Cloud
4. ✅ Add badges to README (build status, license, etc.)
5. ✅ Star your own repository
6. ✅ Share with the community
7. ✅ Enable GitHub Discussions
8. ✅ Add contributing guidelines link
9. ✅ Create project board for tracking issues
10. ✅ Add Wiki documentation

## Creating Your First Release

```bash
# Tag the current commit
git tag -a v1.0.0 -m "Initial release: GRC Multi-Agent Governance System"

# Push the tag
git push origin v1.0.0
```

Then on GitHub:
1. Go to Releases
2. Click "Draft a new release"
3. Select tag v1.0.0
4. Title: "v1.0.0 - Initial Release"
5. Add release notes from PROJECT_SUMMARY.md
6. Attach any compiled binaries or additional files
7. Publish release

## Badge Examples for README

Add these to the top of your README.md:

```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build](https://github.com/HimJoe/policy-as-code/workflows/Python%20Application/badge.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
```

## Success! 🎉

Your GRC Multi-Agent Governance System is now on GitHub and ready to share with the world!

**Repository URL**: https://github.com/HimJoe/policy-as-code

---

Need help? Check the [GitHub Documentation](https://docs.github.com) or create an issue in your repository.
