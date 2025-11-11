from datetime import date

from transcription import Entry, Transcriptable

class Daily(Transcriptable):
    def __init__(self, date: date):
        super().__init__()
        self.date = date

    def accept(self, entry: Entry) -> None:
        if self.transcriptors:
            for transcriptor in self.transcriptors:
                transcriptor.write(entry)