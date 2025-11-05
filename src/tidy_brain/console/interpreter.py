import readline # needed for input history and editing
import transcription as ts

COMMAND_PREFIX = '\\'
DEFAULT_PROJECT = 'Misc'

class Interpreter:
    """REPL interpreter."""

    def __init__(self):
        self.writers = []
        self.commands = {
            'quit': self._exit,
            'q': self._exit,
            'help': self._help,
            'h': self._help,
            'project': self._set_project,
            'p': self._set_project,
        }
        self.current_project = DEFAULT_PROJECT

    def add_writer(self, writer: ts.Writer) -> None:
        """Add a transcription writer."""
        self.writers.append(writer)

    def run(self) -> None:
        """Start the interactive REPL loop."""
        while True:
            try:
                input_entry = input(self._format_prompt()).strip()
                
                if not input_entry:
                    continue
                    
                if input_entry.startswith(COMMAND_PREFIX):
                    self._process_command(input_entry)
                else:
                    self._process_entry(input_entry)
                
            except (KeyboardInterrupt, EOFError):
                self._exit()
            except ValueError:
                self._help()
            except Exception as e:
                print(e)

    def _process_command(self, input_entry: str) -> None:
        """Process a command."""
        command_name, *arguments = input_entry[len(COMMAND_PREFIX):].strip().lower().split()
        if command_name in self.commands:
            self.commands[command_name](arguments)
        else:
            raise ValueError

    def _process_entry(self, input_entry: str) -> None:
        """Process a transcription entry."""
        entry = ts.Entry(content=input_entry, project=self.current_project)
        for writer in self.writers:
            writer.write(entry)

    def _exit(self, arguments: list[str]) -> None:
        """Exit the application."""
        exit(0)
    
    def _help(self, arguments: list[str]) -> None:
        """Display help information."""
        help_text = """Available commands:
\\help or \\h - Show this help message
\\quit or \\q - Exit the application
\\project <name> or \\p <name> - Set the current project (default: Misc)
To add a transcription entry, simply type it and press Enter."""
        print(help_text)

    def _set_project(self, arguments: list[str]) -> None:
        """Set the current project."""
        if arguments:
            self.current_project = arguments[0]
        else:
            self.current_project = DEFAULT_PROJECT

    def _format_prompt(self) -> str:
        """Format the input prompt."""
        prompt = ''
        if self.current_project != DEFAULT_PROJECT:
            prompt = f'[{self.current_project}]'
        prompt += '> '
        return prompt