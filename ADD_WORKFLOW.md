# Adding GitHub Actions Workflow

The GitHub Actions workflow file couldn't be pushed initially due to permission restrictions. Here's how to add it:

## Option 1: Add Directly on GitHub (Easiest)

1. Go to your repository: https://github.com/HimJoe/policyascode
2. Click on **"Actions"** tab
3. Click **"Set up a workflow yourself"**
4. Delete the template and paste the content from `.github/workflows/python-app.yml`
5. Commit the file

## Option 2: Update Your Personal Access Token

If you want to push workflows from command line:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "Policy as Code Workflow"
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. Copy the token
7. Use this token when pushing:

```bash
cd "/Users/himanshujoshi/Downloads/Policiy as a code"
git add .github/workflows/python-app.yml
git commit -m "Add GitHub Actions CI/CD workflow"
git push origin main
```

When prompted for password, use the new token instead.

## Option 3: Add via GitHub Web Interface

1. Go to https://github.com/HimJoe/policyascode
2. Click "Add file" → "Create new file"
3. Name it: `.github/workflows/python-app.yml`
4. Paste the workflow content (see below)
5. Commit directly to main branch

## Workflow File Content

```yaml
name: Python Application

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 pytest pytest-asyncio
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

    - name: Lint with flake8
      run: |
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

    - name: Test import of main modules
      run: |
        python -c "import grc_agent_system"
        python -c "import document_processor"
        python -c "import streamlit_app"
```

## What This Workflow Does

- ✅ Runs on every push and pull request
- ✅ Tests on Python 3.8, 3.9, 3.10, and 3.11
- ✅ Checks code quality with flake8
- ✅ Verifies all modules can be imported
- ✅ Ensures no syntax errors

## Note

This workflow is **optional** but recommended for:
- Continuous Integration (CI)
- Automated testing
- Code quality checks
- Multi-version Python compatibility testing

You can skip it for now and add it later when needed.
