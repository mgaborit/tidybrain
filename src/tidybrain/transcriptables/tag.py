"""Module for tag transcriptables in Tidy Brain application."""
from ..transcription import Entry, Transcriptable

TAG_PREFIX = "#"

class Tag(Transcriptable):
    """Represents a section within a project."""
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def accept(self, entry: Entry) -> None:
        if self.transcriptors and f"{TAG_PREFIX}{self.name}" in entry.content:
            for transcriptor in self.transcriptors:
                transcriptor.write(entry)
