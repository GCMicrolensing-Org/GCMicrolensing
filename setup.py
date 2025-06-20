import setuptools

setuptools.setup(
    name="GCMicrolensing",
    version="0.1.0",
    author="Gregory Costa Cuautle",
    author_email="your_student_email@example.com", # Change this!
    description="Tools for simulating gravitational microlensing events.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GregCuautle/SURP25", # Or wherever the repo lives
    packages=setuptools.find_packages(),
    python_requires='>=3.10', # Based on your environment.yml
    install_requires=[
        "numpy",
        "matplotlib",
        "pandas",
        "scipy",
        "seaborn",
        "astropy",
        "astroquery",
        "pyvo",
        "emcee",
        "corner",
        "requests",
        "tqdm",
        "pybind11",
        "jupyter",
        "ipywidgets",
        "VBMicrolensing",
        # This next line is the magic part that installs the local triplelens
        "TripleLensing @ file:./triplelens"    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Assuming a license
        "Operating System :: OS Independent",
    ],
)