from brain import Brain
from console import Interpreter

CONFIG_FILE = "/home/martin/dev/sandbox/tidy_brain/brain.json"

brain = Brain()
brain.load(CONFIG_FILE)

interpreter = Interpreter(brain)
interpreter.run()
