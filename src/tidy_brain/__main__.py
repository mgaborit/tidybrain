from transcription import DailyWriter
from console import Interpreter

WORKSPACE_DIR = "/home/martin/dev/sandbox/tidy_brain"

daily = DailyWriter(WORKSPACE_DIR)

interpreter = Interpreter()
interpreter.add_writer(daily)
interpreter.run()
