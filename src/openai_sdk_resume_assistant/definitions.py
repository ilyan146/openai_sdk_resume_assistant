"""
This file is to set some config definitions such the root file
"""

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
PACKAGE_DIR = Path(__file__).parent

print(f"ROOT_DIR: {ROOT_DIR}")
print(f"PACKAGE_DIR: {PACKAGE_DIR}")
