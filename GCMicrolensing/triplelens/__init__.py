"""TripleLensing module for GCMicrolensing package."""

import os

# Skip compilation during documentation builds
if os.environ.get('READTHEDOCS') == 'True':
    print("RTD build detected - skipping TripleLensing compilation")
    TripleLensing = None
else:
    try:
        from .TripleLensing import TripleLensing
    except ImportError:
        # If the compiled module is not available, try to build it
        import subprocess
        import sys
        from pathlib import Path

        current_dir = Path(__file__).resolve().parent
        print(f"Building TripleLensing in: {current_dir}")
        print(f"Directory contents: {list(current_dir.iterdir())}")

        try:
            # Check if source files exist
            pymodule_file = current_dir / "pymodule" / "python_bindings.cpp"
            src_file1 = current_dir / "src" / "VBBinaryLensingLibrary.cpp"
            src_file2 = current_dir / "src" / "TripleLensingLibrary.cpp"

            print(f"Checking source files:")
            print(f"  {pymodule_file}: {pymodule_file.exists()}")
            print(f"  {src_file1}: {src_file1.exists()}")
            print(f"  {src_file2}: {src_file2.exists()}")

            if not all([pymodule_file.exists(), src_file1.exists(), src_file2.exists()]):
                print("Warning: Some source files are missing!")
                TripleLensing = None
            else:
                subprocess.check_call(
                    [sys.executable, "setup.py", "build_ext", "--inplace"],
                    cwd=current_dir
                )
                from .TripleLensing import TripleLensing
        except (subprocess.CalledProcessError, ImportError) as e:
            print(f"Warning: Could not import TripleLensing: {e}")
            print("TripleLensing functionality will not be available")
            TripleLensing = None
