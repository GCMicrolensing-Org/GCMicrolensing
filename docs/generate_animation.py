#!/usr/bin/env python3
"""
Script to generate a static animation for the ReadTheDocs homepage.

This script creates an animation of a single-lens microlensing event
and saves it as a GIF file that can be included in the documentation.
"""

import os

from GCMicrolensing.models import OneL1S

# Create a single lens model
model = OneL1S(t0=2450000, tE=20, rho=0.001, u0_list=[0.1, 0.5, 1.0])

# Create _static directory if it doesn't exist
static_dir = "_static"
os.makedirs(static_dir, exist_ok=True)

# Save the animation as a GIF
print("Creating GIF animation...")
animation = model.animate(save_gif=f"{static_dir}/microlensing_animation.gif")
print("GIF saved as 'microlensing_animation.gif'")

# Also test the show_all method with GIF export
print("Creating full animation GIF...")
full_animation = model.show_all(save_gif=f"{static_dir}/full_animation.gif")
print("Full animation GIF saved as 'full_animation.gif'")
