from datetime import datetime

class Entry:
    def __init__(self, content: str, project: str):
        self.timestamp = datetime.now()
        self.project = project
        self.content = content

    def __repr__(self):
        return f"Entry(timestamp={self.timestamp}, project={self.project}, content={self.content})"