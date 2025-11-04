# Publishing the Endercom Python SDK to PyPI

This guide explains how to publish the Endercom Python SDK to PyPI (Python Package Index).

## Prerequisites

1. **PyPI Account**: Create an account at [pypi.org](https://pypi.org) if you don't have one
2. **TestPyPI Account** (optional but recommended): Create an account at [test.pypi.org](https://test.pypi.org) for testing
3. **Build Tools**: Install required build tools:
   ```bash
   pip install --upgrade build twine
   ```

## Pre-Publishing Checklist

1. **Update Version**: Update the version in `pyproject.toml` and `endercom/__init__.py`
2. **Update Changelog**: Document changes (if you maintain a CHANGELOG.md)
3. **Test Locally**: Make sure everything works:
   ```bash
   pip install -e .
   python -c "from endercom import Agent; print('Import successful')"
   ```
4. **Check README**: Ensure README.md renders correctly on PyPI

## Building the Package

Build both source distribution (sdist) and wheel (built distribution):

```bash
cd endercom-python-sdk
python -m build
```

This creates:

- `dist/endercom-1.1.0.tar.gz` (source distribution)
- `dist/endercom-1.1.0-py3-none-any.whl` (wheel)

## Testing on TestPyPI (Recommended)

Before publishing to production PyPI, test on TestPyPI:

### 1. Upload to TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

You'll be prompted for:

- Username: Your TestPyPI username
- Password: Your TestPyPI password (or API token)

### 2. Test Installation from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ endercom
```

### 3. Verify Installation

```python
from endercom import Agent, AgentOptions
print("TestPyPI installation successful!")
```

## Publishing to Production PyPI

### Option 1: Using Twine (Recommended)

```bash
python -m twine upload dist/*
```

You'll be prompted for:

- Username: Your PyPI username (or `__token__` for API tokens)
- Password: Your PyPI password or API token

### Option 2: Using API Token (More Secure)

1. **Create API Token** on PyPI:

   - Go to https://pypi.org/manage/account/token/
   - Create a new API token with scope: "Entire account" or "Project: endercom"
   - Copy the token (starts with `pypi-`)

2. **Upload using token**:
   ```bash
   python -m twine upload dist/*
   ```
   - Username: `__token__`
   - Password: Your API token (pypi-...)

### Option 3: Using .pypirc Config File

Create `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
username = __token__
password = pypi-your-testpypi-token-here
```

Then upload:

```bash
python -m twine upload dist/*
```

## Verifying Publication

After publishing, verify on PyPI:

1. Check package page: https://pypi.org/project/endercom/
2. Test installation:
   ```bash
   pip install endercom
   ```
3. Verify import:
   ```python
   from endercom import Agent
   print(Agent.__module__)
   ```

## Updating the Package

To publish a new version:

1. Update version in `pyproject.toml` and `endercom/__init__.py`
2. Build new distributions:
   ```bash
   python -m build
   ```
3. Upload:
   ```bash
   python -m twine upload dist/*
   ```

## Version Format

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.1.0)
- Update version in both:
  - `pyproject.toml`: `version = "1.1.0"`
  - `endercom/__init__.py`: `__version__ = "1.1.0"`

## Troubleshooting

### "Package already exists" error

- The version you're trying to publish already exists
- Increment the version number

### "Invalid credentials"

- Check your username/password
- For API tokens, use `__token__` as username

### "File already exists"

- Clear the `dist/` folder and rebuild:
  ```bash
  rm -rf dist/ build/ *.egg-info
  python -m build
  ```

### "Repository not found"

- Ensure you're using the correct repository URL
- Check your `.pypirc` or command-line arguments

## Security Best Practices

1. **Use API Tokens**: Prefer API tokens over passwords
2. **Don't Commit Secrets**: Never commit `.pypirc` or tokens to git
3. **Use CI/CD**: Consider automating publishing via GitHub Actions
4. **Two-Factor Authentication**: Enable 2FA on your PyPI account

## Automated Publishing (GitHub Actions)

A GitHub Actions workflow is included in `.github/workflows/publish.yml`. To use it:

1. Add `PYPI_API_TOKEN` to your GitHub repository secrets
2. Create a GitHub release to trigger automatic publishing

## Quick Reference

```bash
# Build
python -m build

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*

# Clean build artifacts
rm -rf dist/ build/ *.egg-info
```
