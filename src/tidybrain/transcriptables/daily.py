"""Module for daily transcriptions in Tidy Brain application."""
from datetime import date

from ..transcription import Entry, Transcriptable

class Daily(Transcriptable):
    """Represents daily transcriptions."""
    def __init__(self, daily_date: date):
        super().__init__()
        self.date = daily_date

    def accept(self, entry: Entry) -> None:
        if self.transcriptors:
            for transcriptor in self.transcriptors:
                transcriptor.write(entry)
