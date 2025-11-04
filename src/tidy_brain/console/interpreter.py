import transcription as ts

class Interpreter:
    """REPL interpreter."""

    def __init__(self):
        self.writers = []
        self.commands = {
            'exit': self._exit,
        }

    def add_writer(self, writer: ts.Writer) -> None:
        """Add a transcription writer."""
        self.writers.append(writer)

    def run(self) -> None:
        """Start the interactive REPL loop."""
        while True:
            try:
                input_entry = input(">>> ").strip()
                
                if not input_entry:
                    continue
                    
                self._process_input(input_entry)
                
            except (KeyboardInterrupt, EOFError):
                self._exit(self)

    def _process_input(self, input_entry: str) -> None:
        """Process the user input."""
        command_candidate = input_entry.lower()
        if command_candidate in self.commands:
            self.commands[command_candidate]()
        else:
            entry = ts.Entry(content=input_entry)
            for writer in self.writers:
                writer.write(entry)

    def _exit(self) -> None:
        """Exit the application."""
        exit(0)