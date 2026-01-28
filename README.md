# CI Starter

Learn GitHub Actions by building a CI pipeline for a Python project.

> **Part of a 4-project series!** This repo grows with you:
> 1. **Project 1** (this one): Basic CI workflow
> 2. **Project 2**: AI code review on every PR
> 3. **Project 3**: AI test generator
> 4. **Project 4**: AI stale code detector

## What You'll Do

1. **Write Python code** - Add functions to `app.py`
2. **Write tests** - Add test cases to `tests/test_app.py`
3. **Create CI workflow** - Build `.github/workflows/ci.yml`
4. **Watch it run** - Push and see GitHub Actions in action!

## Getting Started

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ci-starter.git
cd ci-starter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Your Missions

### Mission 1: Add a Function

Add a `multiply` function to `app.py`:

```python
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    # Your code here
```

### Mission 2: Add Tests

Add a `TestMultiply` class to `tests/test_app.py`:

```python
class TestMultiply:
    def test_multiply_positive(self):
        # Your test here

    def test_multiply_by_zero(self):
        # Your test here
```

### Mission 3: Create CI Workflow

Create `.github/workflows/ci.yml` that:
- Triggers on push and pull_request to main
- Runs on ubuntu-latest
- Checks out code
- Sets up Python 3.11
- Installs dependencies
- Runs linter (`ruff check .`)
- Runs tests (`pytest -v`)

### Mission 4: Break It, Fix It

1. Push your code → watch it pass ✅
2. Break a test intentionally → watch it fail ❌
3. Fix the test → watch it pass again ✅

### Secret Mission: Build Artifact

Add steps to build and upload a dist/ artifact!

## Local Commands

```bash
pytest -v        # Run tests
ruff check .     # Run linter
python -m build  # Build package
```

## Project Structure

```
ci-starter/
├── .github/workflows/
│   └── ci.yml            # Project 1: You create this!
├── scripts/              # Projects 2-4: AI scripts go here
├── tests/test_app.py     # Add more tests!
├── app.py                # Add more functions!
├── requirements.txt
└── pyproject.toml
```

## Troubleshooting Guide

### Common Errors & Solutions

Below are real errors encountered during setup and their solutions:

---

#### Error 1: Git User Identity Not Configured

**Error Message:**
```
Author identity unknown
*** Please tell me who you are.
fatal: unable to auto-detect email address
```

![Error 1](Error-pics/error%201.png)

**What Happened:**
When trying to commit changes, git doesn't know who you are. Git requires a username and email to associate with commits.

**Solution:**
Configure your git identity globally:

```bash
git config --global user.name "your-github-username"
git config --global user.email "your-email@example.com"
```

![Error 1 Fixed](Error-pics/error%201%20fixed.png)

**Prevention:** Always configure git when setting up a new machine or development environment.

---

#### Error 2: Empty Workflow Files on Main Branch

**Error Message:**
```
Error: No event triggers defined in `on`
```

![Error 2](Error-pics/error%202.png)

**What Happened:**
The workflow files (`.github/workflows/pr-review.yml` and `.github/workflows/test-gen.yml`) existed on the main branch but were **empty**. When GitHub tries to run workflows for a PR, it uses the workflow files from the target branch (main), not the source branch. Since they were empty, GitHub couldn't find any trigger events.

**Root Cause:**
The workflow files were created but never properly populated with content on the main branch. This happened because:
1. Files were created with placeholders
2. Content was added to the feature branch
3. But the main branch still had empty files

![Error 2 Diagnosis](Error-pics/error%202.1.png)

**Solution:**
1. Switch to main branch
2. Add proper workflow content to both files
3. Commit and push to main

```bash
git checkout main
# Edit .github/workflows/pr-review.yml and test-gen.yml with proper content
git add .github/workflows/
git commit -m "Fix empty workflow files on main branch"
git push origin main
```

![Error 2 Fix](Error-pics/error%202.1%20poss%20fix.png)

The workflow files need to have the complete YAML configuration including:
- `name:` - Workflow name
- `on:` - Trigger events (pull_request, push, etc.)
- `jobs:` - The actual jobs to run

![Error 2 Fix Explained](Error-pics/error%202.1%20poss%20fix%20explained.png)

---

#### Error 3: Workflow Files on Feature Branch

**Error Message:**
```
Error: No event triggers defined in `on`
(When pushing to feature branch)
```

![Error 3](Error-pics/error%203.png)

**What Happened:**
The workflow files existed on BOTH the main branch AND the feature branch. When pushing to the feature branch, GitHub tried to run the workflows from that branch. However:
- `pr-review.yml` is configured to trigger ONLY on `pull_request` events
- Pushing to a branch triggers a `push` event, not a `pull_request` event
- GitHub complained because it was trying to run a workflow that had no matching trigger

**Solution:**
Remove workflow files from the feature branch since they should only exist on the target branch (main):

```bash
git checkout feature/new-function
git rm .github/workflows/pr-review.yml .github/workflows/test-gen.yml
git commit -m "Remove workflow files from feature branch"
git push
```

![Error 3 Fix](Error-pics/error%203%20fix%20replaced%20code%20in%202%20files.png)

**Best Practice:** 
- Workflow files for PRs should live on the target branch (usually `main`)
- Don't include `.github/workflows/` files in feature branches unless you specifically need them
- PR workflows will use the configuration from the target branch, not the source branch

![Error 3 Success](Error-pics/error%203%20its%20working.png)

---

### Success Checklist

After fixing all errors, you should see:

✅ Green checkmarks on your PR
✅ AI Code Review bot comment with analysis
✅ AI Test Generation completing successfully
✅ All workflow runs passing

---

## Tips for Success

1. **Always configure git first:**
   ```bash
   git config --global user.name "username"
   git config --global user.email "email@example.com"
   ```

2. **Keep workflow files on main branch only** (for PR workflows)

3. **Check workflow files aren't empty:**
   ```bash
   cat .github/workflows/pr-review.yml  # Should show content, not empty
   ```

4. **Create actual PRs** - Workflows only trigger on real PR events, not just pushes

5. **Wait for workflows to complete** - Give them 1-2 minutes to run

6. **Check the Actions tab** for detailed logs if something fails
