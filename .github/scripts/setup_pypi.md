# PyPI Publishing Setup Guide

This guide explains how to set up automatic publishing to TestPyPI and PyPI when you create git tags.

## Prerequisites

1. **TestPyPI Account**: Create an account at https://test.pypi.org/
2. **PyPI Account**: Create an account at https://pypi.org/
3. **API Tokens**: Generate API tokens for both services

## Step 1: Generate API Tokens

### TestPyPI Token
1. Go to https://test.pypi.org/manage/account/token/
2. Click "Add API token"
3. Give it a name like "GCMicrolensing TestPyPI"
4. Select "Entire account (all projects)"
5. Copy the token (it starts with `pypi-`)

### PyPI Token
1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Give it a name like "GCMicrolensing PyPI"
4. Select "Entire account (all projects)"
5. Copy the token (it starts with `pypi-`)

## Step 2: Add GitHub Secrets

1. Go to your GitHub repository
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add these two secrets:

   **Name**: `TEST_PYPI_API_TOKEN`
   **Value**: Your TestPyPI token (starts with `pypi-`)

   **Name**: `PYPI_API_TOKEN`
   **Value**: Your PyPI token (starts with `pypi-`)

## Step 3: Test the Setup

1. Create a test tag:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```

2. Check the GitHub Actions tab to see the workflow running
3. Verify the package appears on TestPyPI: https://test.pypi.org/project/GCMicrolensing/
4. Verify the package appears on PyPI: https://pypi.org/project/GCMicrolensing/

## Step 4: Install from PyPI

Once published, users can install your package with:

```bash
# From TestPyPI (for testing)
pip install -i https://test.pypi.org/simple/ GCMicrolensing

# From PyPI (production)
pip install GCMicrolensing
```

## Troubleshooting

### Common Issues

1. **Package name conflict**: If `GCMicrolensing` is taken, update the name in `pyproject.toml`
2. **Build errors**: Check that all dependencies are properly specified
3. **Authentication errors**: Verify your API tokens are correct and have proper permissions

### Manual Publishing (if needed)

If you need to publish manually:

```bash
# Build the package
python -m build

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

## Security Notes

- Never commit API tokens to your repository
- Use GitHub secrets to store sensitive information
- Regularly rotate your API tokens
- Use TestPyPI for testing before publishing to PyPI

## Workflow Details

The GitHub Actions workflow will:

1. **Test**: Run your test suite
2. **Build**: Create source and wheel distributions
3. **Release**: Create a GitHub release with assets
4. **Publish to TestPyPI**: Upload to test.pypi.org
5. **Publish to PyPI**: Upload to pypi.org

All steps run automatically when you push a tag starting with `v` (e.g., `v1.0.0`).
