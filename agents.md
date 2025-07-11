# GCMicrolensing - AI Agent Guidelines

## Repository Overview

This is a Python package for simulating gravitational microlensing events with single, binary, and triple lens systems. The package uses custom C++ libraries (TripleLensing) and provides both photometric and astrometric calculations.

## Key Architecture Decisions

### 1. Package Structure
- **Main package**: `GCMicrolensing/` contains the core functionality
- **Custom dependency**: `triplelens/` is a modified version of TripleLensing with Greg's custom changes
- **Hybrid packaging**: Uses both `pyproject.toml` (modern) and `setup.py` (for local TripleLensing dependency)

### 2. Dependencies
- **TripleLensing**: Custom C++ library with pybind11 bindings (local file dependency)
- **VBMicrolensing**: For binary lens calculations
- **Standard scientific stack**: numpy, matplotlib, scipy, astropy, etc.

## Coding Standards

### 1. Documentation Style
- **Use NumPyDoc style** for all docstrings
- **Include comprehensive examples** in docstrings
- **Document all parameters, returns, and attributes**
- **Add mathematical background** where relevant

Example docstring structure:
```python
def method_name(self, param1, param2):
    """
    Brief description of what the method does.
    
    Parameters
    ----------
    param1 : float
        Description of parameter 1.
    param2 : array-like
        Description of parameter 2.
    
    Returns
    -------
    result : ndarray
        Description of return value.
    
    Examples
    --------
    Basic usage:
    
    >>> model = ModelClass(param1=1.0, param2=[0.1, 0.5])
    >>> result = model.method_name(1.0, [0.1, 0.5])
    
    Notes
    -----
    Additional implementation details, mathematical background, etc.
    """
```

### 2. Import Conventions
- **Use relative imports** for internal package modules: `from .TestML import ...`
- **Never use self-imports** within a file (e.g., `from TestML import ...` in TestML.py)
- **Group imports**: standard library, third-party, local

### 3. Class Design
- **All model classes** inherit similar patterns but are independent
- **Use `__init__`** for parameter validation and setup
- **Include plotting methods** for visualization
- **Support multiple impact parameters** via `u0_list`

## Important Idiosyncrasies

### 1. TripleLensing Integration
- **Custom modifications**: Greg has modified the original TripleLensing code
- **Local installation**: Uses `file://` URL in setup.py for local dependency
- **C++ compilation**: Requires pybind11 and C++ compiler
- **Build artifacts**: Excluded from git via .gitignore

### 2. Dual Backend Support
- **VBMicrolensing**: Used for binary lens calculations and some triple lens features
- **TripleLensing**: Used for advanced triple lens calculations and image finding
- **Cross-validation**: Some classes support both backends for comparison

### 3. Animation and Visualization
- **Matplotlib animations**: Used for interactive visualizations
- **IPython.display.HTML**: For Jupyter notebook compatibility
- **Multiple plot types**: Light curves, centroid shifts, caustic curves, critical curves

### 4. Parameter Naming
- **Consistent naming**: `t0`, `tE`, `rho`, `u0_list` across all models
- **Angle parameters**: Some use degrees (`alpha_deg`), others radians (`alpha`)
- **Mass ratios**: `q` for binary, `q2`, `q3` for triple lenses
- **Separations**: `s` for binary, `s2`, `s3` or `s12`, `s23` for triple lenses

## Release Process

### 1. Version Management
- **Update version** in `pyproject.toml`
- **Create git tag**: `git tag v1.0.0`
- **Push tag**: `git push origin v1.0.0`
- **Automated release**: GitHub Actions creates release and assets

### 2. Distribution
- **Source distribution**: .tar.gz file
- **Wheel distribution**: .whl file
- **GitHub release**: Automatic with assets
- **PyPI publishing**: Optional (commented in workflow)

### 3. Testing
- **Smoke tests**: Basic instantiation and plotting
- **CI/CD**: Runs on every push and pull request
- **Release testing**: Full test suite before release

## Development Workflow

### 1. Local Development
```bash
# Install in development mode
pip install -e .

# Run tests
pytest tests/

# Build package
python -m build
```

### 2. Documentation
- **Sphinx docs**: Located in `docs/`
- **Read the Docs**: Configured for automatic deployment
- **API documentation**: Auto-generated from docstrings

### 3. Code Quality
- **Type hints**: Use where appropriate
- **Error handling**: Graceful degradation for edge cases
- **Performance**: Optimize for scientific computing workloads

## Common Pitfalls

### 1. Import Errors
- **Circular imports**: Avoid self-imports within files
- **Relative imports**: Use `.` for same-package imports
- **Missing dependencies**: Ensure TripleLensing is properly installed

### 2. C++ Compilation
- **pybind11**: Required for TripleLensing
- **Compiler flags**: May need adjustment for different platforms
- **Build artifacts**: Clean up after development

### 3. Scientific Accuracy
- **Parameter validation**: Check physical constraints
- **Numerical stability**: Handle edge cases in lensing calculations
- **Unit consistency**: Ensure all calculations use consistent units

## AI Agent Guidelines

### 1. Before Making Changes
- **Understand the physics**: Gravitational microlensing involves complex mathematical calculations
- **Test thoroughly**: Changes can affect scientific accuracy
- **Maintain compatibility**: Don't break existing API without good reason
- **Document changes**: Update docstrings and examples

### 2. When Adding Features
- **Follow existing patterns**: Use similar structure to existing model classes
- **Include examples**: Add comprehensive usage examples in docstrings
- **Add tests**: Create corresponding test cases
- **Update documentation**: Modify relevant documentation files

### 3. When Fixing Bugs
- **Understand the root cause**: Scientific bugs can be subtle
- **Test edge cases**: Lensing calculations have many edge cases
- **Verify accuracy**: Ensure fixes don't introduce new errors
- **Update examples**: Fix any broken examples in docstrings

### 4. Code Review Checklist
- [ ] Docstrings follow NumPyDoc style
- [ ] Examples are comprehensive and accurate
- [ ] Mathematical notation is correct
- [ ] Error handling is appropriate
- [ ] Performance is acceptable
- [ ] Tests pass
- [ ] Documentation is updated

## Repository-Specific Notes

### 1. File Organization
- `GCMicrolensing/models.py`: Main model classes
- `GCMicrolensing/TestML.py`: Helper functions for TripleLensing
- `triplelens/`: Custom TripleLensing library
- `docs/`: Sphinx documentation
- `tests/`: Test suite
- `.github/workflows/`: CI/CD workflows

### 2. Configuration Files
- `pyproject.toml`: Modern package configuration
- `setup.py`: Legacy configuration for local dependencies
- `MANIFEST.in`: Include triplelens directory in distribution
- `.gitignore`: Exclude build artifacts and temporary files

### 3. Dependencies
- **Core scientific**: numpy, matplotlib, scipy, astropy
- **Specialized**: VBMicrolensing, TripleLensing (custom)
- **Development**: pytest, sphinx, build tools
- **System**: ffmpeg (for animations)

This repository represents a sophisticated scientific computing package with complex dependencies and careful attention to accuracy and usability. Always prioritize scientific correctness and maintain the high standard of documentation and examples.
