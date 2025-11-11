import readline # needed for input history and editing

from brain import Brain
from transcription import ContextKeys, Entry

COMMAND_PREFIX = '\\'

class Interpreter:
    """REPL interpreter."""

    def __init__(self, brain: Brain):
        self.commands = {
            'quit': self._exit,
            'q': self._exit,
            'help': self._help,
            'h': self._help,
            'project': self._set_project,
            'p': self._set_project,
        }
        self.context = {}
        self.brain = brain

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
                    entry = Entry(content=input_entry, context=self.context.copy())
                    self.brain.process(entry)
                
            except (KeyboardInterrupt, EOFError):
                self._exit()
            except Exception as e:
                print(e)

    def _process_command(self, input_entry: str) -> None:
        """Process a command."""
        command_name, *arguments = input_entry[len(COMMAND_PREFIX):].strip().lower().split()
        if command_name in self.commands:
            self.commands[command_name](arguments)
        else:
            raise ValueError(f"Unknown command: {command_name}")

    def _exit(self, arguments: list[str]) -> None:
        """Exit the application."""
        exit(0)
    
    def _help(self, arguments: list[str]) -> None:
        """Display help information."""
        help_text = """Available commands:
\\help|\\h - Show this help message
\\quit|\\q - Exit the application
\\project|\\p <project_name>[/<>section_name>] - Set the current project and section (default: None)
To add a transcription entry, simply type it and press Enter."""
        print(help_text)

    def _set_project(self, arguments: list[str]) -> None:
        """Set the current project."""
        if len(arguments) > 1:
            raise ValueError(f"Too many arguments, usage: \\project|\\p <project_name>[/<>section_name>]")

        if arguments:
            arguments = arguments[0].split('/', 1)
            project_name = arguments[0]
            section_name = arguments[1] if len(arguments) > 1 else None
            if project_name not in self.brain.projects:
                raise ValueError(f"Unknown project: {project_name}")
            project = self.brain.projects[project_name]
            if section_name and section_name not in project.sections:
                raise ValueError(f"Unknown section: {section_name} in project '{project_name}'")
            
            self.context[ContextKeys.PROJECT] = project_name
            if section_name:
                self.context[ContextKeys.SECTION] = section_name
            else:
                self.context.pop(ContextKeys.SECTION, None)
        else:
            self.context.pop(ContextKeys.PROJECT, None)
            self.context.pop(ContextKeys.SECTION, None)

    def _format_prompt(self) -> str:
        """Format the input prompt."""
        prompt = ""
        project_name = self.context.get(ContextKeys.PROJECT)
        if project_name:
            prompt += project_name
            section_name = self.context.get(ContextKeys.SECTION)
            if section_name:
                prompt += f"/{section_name}"
        prompt += "> "
        return prompt