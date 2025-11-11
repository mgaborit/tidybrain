import os

from transcription import Entry, Transcriptor

class FileTranscriptor(Transcriptor):
    """Base class for file-based transcription handlers."""
    def __init__(self,  file_path: str):
        self.file_path = file_path

    def write(self, entry: Entry) -> None:
        """Write a transcription entry to the appropriate file."""
        with open(self.file_path, self._ensure_file_exists(), encoding='utf-8') as file:
            file.write(str(entry))

    def _ensure_file_exists(self) -> str:
        """Initialize the transcription file."""
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
        return 'a' if os.path.isfile(self.file_path) else 'w'
