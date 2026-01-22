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
