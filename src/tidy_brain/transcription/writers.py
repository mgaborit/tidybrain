from datetime import datetime
import os

from . import Entry

class Writer:
    def __init__(self,  base_dir: str):
        self.base_dir = base_dir

    def write(self, entry: Entry) -> None:
        with open(self._get_file_path(entry), self._ensure_file_exists(entry), encoding='utf-8') as file:
            file.write(self._format_line(entry))

    def _ensure_file_exists(self, entry: Entry) -> str:
        """Initialize the transcription file."""
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        return 'a' if os.path.isfile(self._get_file_path(entry)) else 'w'

    def _format_line(self, entry: Entry) -> str:
        """Format a transcription entry."""
        raise NotImplementedError

    def _get_file_path(self, entry: Entry) -> str:
        """Get the full file path for the transcription file."""
        raise NotImplementedError

class DailyWriter(Writer):
    def __init__(self, workspace_dir: str):
        super().__init__(os.path.join(workspace_dir, 'daily'))

    def _get_file_path(self, entry: Entry) -> str:
        """Get the full file path for the transcription file."""
        return os.path.join(self.base_dir, f'{entry.timestamp.date().isoformat()}.txt')

    def _format_line(self, entry: Entry) -> str:
        """Format a transcription entry."""
        return f"[{entry.timestamp.isoformat(timespec='minutes', sep=' ')}]\t{entry.content}\n"
