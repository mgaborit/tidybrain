"""Module for transcription handling in Tidy Brain application."""
import abc
from datetime import datetime

class ContextKeys:
    """Constants for context dictionary keys."""
    PROJECT = 'project'
    SECTION = 'section'

class Entry:
    """Class representing a transcription entry."""
    def __init__(self, content: str, context: dict[str, str] | None = None):
        self.timestamp = datetime.now()
        self.content = content
        self.context = context

    def __str__(self):
        timestamp_part = f'[{self.timestamp.isoformat(timespec="minutes", sep=" ")}]'

        project_part = ''
        if self.context:
            project = self.context.get(ContextKeys.PROJECT)
            section = self.context.get(ContextKeys.SECTION)
            if project:
                project_part += f'({project}'
                if section:
                    project_part += f'/{section}'
                project_part += ')'

        return f'{timestamp_part} {project_part} {self.content}\n'


class Transcriptor(metaclass=abc.ABCMeta):
    """Base class for transcription handlers."""

    @abc.abstractmethod
    def write(self, entry: Entry) -> None:
        """Write a transcription entry to the appropriate location."""
        raise NotImplementedError("Subclasses must implement this method.")

class Transcriptable(metaclass=abc.ABCMeta):
    """Interface for objects that can be transcribed."""
    def __init__(self):
        self.transcriptors: list[Transcriptor] | None = None

    def register(self, transcriptor: Transcriptor) -> None:
        """Register a transcriptor to handle transcription."""
        if self.transcriptors is None:
            self.transcriptors = []
        self.transcriptors.append(transcriptor)

    @abc.abstractmethod
    def accept(self, entry: Entry) -> None:
        """Transcribe the entry if it matches certain criteria."""
        raise NotImplementedError("Subclasses must implement this method.")
