"""Module for project transcriptables in Tidy Brain application."""
from ..transcription import ContextKeys, Entry, Transcriptable

class Project(Transcriptable):
    """Represents a project."""
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.sections: dict[str, Section] = {}

    def accept(self, entry: Entry) -> None:
        if entry.context \
            and entry.context.get(ContextKeys.PROJECT) == self.name:
            section_name = entry.context.get(ContextKeys.SECTION)
            if self.sections \
                and section_name \
                and section_name in self.sections:
                self.sections[section_name].accept(entry)
            else:
                if self.transcriptors:
                    for transcriptor in self.transcriptors:
                        transcriptor.write(entry)

class Section(Transcriptable):
    """Represents a section within a project."""
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def accept(self, entry: Entry) -> None:
        if self.transcriptors \
            and entry.context \
            and entry.context.get(ContextKeys.SECTION) == self.name:
            for transcriptor in self.transcriptors:
                transcriptor.write(entry)
