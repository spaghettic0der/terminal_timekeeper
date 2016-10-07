import os
from project import *
import json


class JsonHelper:
    def __init__(self, filename):
        self.filename = filename
        self.json = None

    def get_json(self):
        if os.path.isfile(self.filename):
            with open(self.filename) as f:
                return json.load(f)

    def save(self, content):
        with open(self.filename, "w") as f:
            f.write(json.dumps(content, sort_keys=True, indent=4))

    def save_json(self, timekeeper):
        json_project_array = []
        for project in timekeeper.projects:
            current_json_project = project.to_json()
            json_project_array.append(current_json_project)

        json_task_array = []
        for task in timekeeper.get_all_tasks():
            current_json_task = task.to_json()
            json_task_array.append(current_json_task)

        save_object = {
            "saveProjectArray": json_project_array,
            "saveObjectArray": json_task_array
        }
        self.save(save_object)

    def get_projects_from_json(self):
        """loads objects from json into memory"""
        self.json = self.get_json()
        projects = []
        projects_json = self.json["saveProjectArray"]
        """all tasks from all projects"""
        task_list_json = self.json["saveObjectArray"]
        for current_project_json in projects_json:
            project_name = current_project_json["name"]
            project = Project(project_name)
            try:
                project.frozen = current_project_json["frozen"]
                project.tags = current_project_json["tags"]
            except KeyError:
                pass
            for task_json in task_list_json:
                if task_json["projectName"] == project_name:
                    task_name = task_json["taskName"]
                    start_time = TimeHelper.get_time_in_s(json_time=task_json["startTime"])
                    end_time = TimeHelper.get_time_in_s(json_time=task_json["endTime"])
                    duration = task_json["durationInSec"]
                    task_uuid = task_json["UUID"]
                    task = Task(task_name, project_name)
                    task.start_time = start_time
                    task.end_time = end_time
                    task.duration = duration
                    task.uuid = task_uuid
                    project.task_list.append(task)
            projects.append(project)
        return projects
