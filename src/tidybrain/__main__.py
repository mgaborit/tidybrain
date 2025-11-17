"""Entry point for Tidy Brain application."""
import os
import sys

from .brain import Brain
from .console import Interpreter

HOME_DIR = os.environ.get("TB_HOME")
if HOME_DIR is None:
    print("Tidy Brain home directory is not set. Please set the TB_HOME environment variable.")
    sys.exit(1)

if not os.path.exists(HOME_DIR):
    os.makedirs(HOME_DIR)

CONFIG_FILE = os.path.join(HOME_DIR, "brain.json")

brain = Brain()
brain.load(CONFIG_FILE)

interpreter = Interpreter(brain)
interpreter.run()
