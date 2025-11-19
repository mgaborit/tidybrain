"""Module for managing the workspace in Tidy Brain application."""
from datetime import date
import json
import os
from typing import Any

from .transcription import Entry
from .transcriptables import Daily, Person, Project, Section, Tag
from .transcriptors.file import FileTranscriptor

class Brain:
    """Represents a workspace for managing projects and their transcriptions."""

    def __init__(self):
        self.daily = Daily(date.today())
        self.projects: dict[str, Project] = {}
        self.tags: dict[str, Tag] = {}
        self.persons: dict[str, Person] = {}

    def process(self, entry: Entry) -> None:
        """Process a transcription entry."""
        self.daily.accept(entry)
        for project in self.projects.values():
            project.accept(entry)
        for tag in self.tags.values():
            tag.accept(entry)
        for person in self.persons.values():
            person.accept(entry)

    def load(self, config_file: str):
        """Load workspace configuration."""
        workspace_dir = os.path.dirname(config_file)

        with open(config_file, 'r', encoding='utf-8') as file:
            configuration = json.load(file)

        self._load_projects(configuration, workspace_dir)
        self._load_tags(configuration, workspace_dir)
        self._load_persons(configuration, workspace_dir)

    def _load_projects(self, configuration: Any, workspace_dir: str) -> None:
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
                        project_config.get('filename', f'{project.name}.txt')
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

    def _load_tags(self, configuration: Any, workspace_dir: str) -> None:
        tags_dir = os.path.join(workspace_dir, configuration.get('tags_dir', 'tags'))
        for tag_config in configuration.get('tags', []):
            tag = Tag(tag_config['name'])
            tag.register(
                FileTranscriptor(
                    os.path.join(
                        tags_dir,
                        tag_config.get('filename', f'{tag.name}.txt')
                    )))
            self.tags[tag.name] = tag

    def _load_persons(self, configuration: Any, workspace_dir: str) -> None:
        persons_dir = os.path.join(workspace_dir, configuration.get('persons_dir', 'people'))
        for person_config in configuration.get('persons', []):
            person = Person(
                short_name=person_config['short_name'],
                full_name=person_config.get('full_name', ""),
                email=person_config.get('email', "")
            )
            default_filename = f'{person.short_name
                                  if len(person.full_name) == 0
                                  else person.full_name}.txt'
            person.register(
                FileTranscriptor(
                    os.path.join(
                        persons_dir,
                        person_config.get('filename', default_filename)
                    )))
            self.persons[person.short_name] = person
