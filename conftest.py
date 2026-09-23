# -*- coding: utf-8 -*-
"""Ensures the project root is importable when running `pytest tests/`
from anywhere, without needing an editable install."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
