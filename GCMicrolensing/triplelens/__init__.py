"""TripleLensing module for GCMicrolensing package."""

try:
    from .TripleLensing import TripleLensing
except ImportError:
    # If the compiled module is not available, try to build it
    import subprocess
    import sys
    from pathlib import Path

    current_dir = Path(__file__).resolve().parent
    try:
        subprocess.check_call(
            [sys.executable, "setup.py", "build_ext", "--inplace"], cwd=current_dir
        )
        from .TripleLensing import TripleLensing
    except (subprocess.CalledProcessError, ImportError) as e:
        print(f"Warning: Could not import TripleLensing: {e}")
        print("TripleLensing functionality will not be available")
        TripleLensing = None
