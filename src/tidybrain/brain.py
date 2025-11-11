"""Module for managing the workspace in Tidy Brain application."""
from datetime import date
import json
import os

from .transcription import Entry
from .transcriptables import Daily, Project, Section
from .transcriptors.file import FileTranscriptor

class Brain:
    """Represents a workspace for managing projects and their transcriptions."""

    def __init__(self):
        self.daily = Daily(date.today())
        self.projects: dict[str, Project] = {}

    def process(self, entry: Entry) -> None:
        """Process a transcription entry."""
        self.daily.accept(entry)
        for project in self.projects.values():
            project.accept(entry)

    def load(self, config_file: str):
        """Load workspace configuration."""
        workspace_dir = os.path.dirname(config_file)

        with open(config_file, 'r', encoding='utf-8') as file:
            configuration = json.load(file)

        daily_dir = os.path.join(workspace_dir, configuration.get('daily_dir', 'daily'))
        self.daily.register(
            FileTranscriptor(
                os.path.join(
                    daily_dir,
                    f'{self.daily.date.isoformat()}.txt'
                )))

        projects_dir = os.path.join(workspace_dir, configuration.get('projects_dir', 'projects'))
        for project_config in configuration.get('projects', []):
            project = Project(project_config['name'])
            project_path = project_config.get('path', project.name)
            project.register(
                FileTranscriptor(
                    os.path.join(
                        projects_dir,
                        project_path,
                        project_config.get('filename', 'project.txt')
                    )))
            self.projects[project.name] = project

            for section_config in project_config.get('sections', []):
                section = Section(section_config['name'])
                section.register(
                    FileTranscriptor(
                        os.path.join(
                            projects_dir,
                            project_path,
                            section_config.get('filename', f'{section.name}.txt')
                        )))
                project.sections[section.name] = section
