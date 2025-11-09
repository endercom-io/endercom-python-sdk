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

## Testing Locally (Recommended)

Before publishing to production PyPI, test locally:

```bash
# Build the package
python -m build

# Install from local wheel
pip install dist/endercom-*.whl

# Or install in editable mode for development
pip install -e .

# Test the installation
python -c "from endercom import Agent, AgentOptions; print('Import successful!')"

# Run your tests (if you have them)
python -m pytest  # optional
```

## Testing on TestPyPI (Optional)

**Note**: TestPyPI can have package name conflicts (403 errors are common). If you encounter issues, skip TestPyPI and test locally instead (see above).

If you want to try TestPyPI:

### 1. Get TestPyPI API Token

- Go to https://test.pypi.org/manage/account/token/
- Create a new API token (separate from production PyPI token)

### 2. Upload to TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

You'll be prompted for:

- Username: `__token__`
- Password: Your TestPyPI API token (starts with `pypi-`)

### 3. Test Installation from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ endercom
```

### 4. Verify Installation

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

### "403 Forbidden" Error on TestPyPI

This is a **very common issue** and can happen for several reasons:

1. **Package name already exists on TestPyPI**:

   - TestPyPI and PyPI are separate registries
   - Even if the package doesn't exist on production PyPI, it might exist on TestPyPI
   - Someone else may have already claimed the name for testing
   - **Solution**: Skip TestPyPI and test locally instead (see below)

2. **Wrong API token**:

   - TestPyPI requires a **separate API token** from production PyPI
   - Make sure you're using a TestPyPI token, not a production PyPI token
   - **Solution**: Create a new token at https://test.pypi.org/manage/account/token/

3. **Token scope issues**:
   - Ensure your token has the correct scope/permissions
   - **Solution**: Create a new token with "Entire account" scope

**Recommended Workaround**: Skip TestPyPI and test locally:

```bash
# Build the package
python -m build

# Install locally to test
pip install dist/endercom-*.whl

# Test the installation
python -c "from endercom import Agent; print('Success!')"

# If everything works, publish directly to production PyPI
python -m twine upload dist/*
```

### "Package already exists" error

- The version you're trying to publish already exists
- Increment the version number in both `pyproject.toml` and `endercom/__init__.py`

### "Invalid credentials"

- Check your username/password
- For API tokens, use `__token__` as username
- Make sure you're using the correct token for the correct registry (TestPyPI vs PyPI)

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
