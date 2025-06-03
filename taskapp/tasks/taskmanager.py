from typing import Optional, List
from uuid import UUID

from taskapp.tasks.task import Task
from taskapp.tasks.TaskErrors import ParentIdNotFoundError, TaskIdNotFoundError
from taskapp.storage.filedb import FileDB


class TaskManager:
    def __init__(self, filedb: FileDB):
        self.tasks: List[Task] = []
        self.db = filedb
        self.load()

    def load(self):
        self.tasks = [Task.from_dict(t) for t in self.db.load()]

    def save(self):
        self.db.save([t.to_dict() for t in self.tasks])

    def add_task(self, title, parent_id=None):
        if parent_id:
            if not self.get_task(parent_id):
                raise ParentIdNotFoundError
        task = Task(title, parent_id=parent_id)
        self.tasks.append(task)
        self.save()
        return task

    def get_task(self, task_id) -> Optional[Task]:
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

    def find_by_title(self, title: str) -> List[Task]:
        found = []
        for t in self.tasks:
            if title in t.title:
                found.append(t)
        for t in self.tasks:
            if title.lower() in t.title.lower():
                found.append(t)
        return found

    def mark_done(self, task_id):
        task = self.get_task(task_id)
        if task is None:
            raise TaskIdNotFoundError
        task.finish()
        self.save()
        return task
    
    def toggle(self, task_id):
        task = self.get_task(task_id)
        if task is None:
            raise TaskIdNotFoundError
        task.toggle()
        self.save()
        return task

    def delete(self, task_id):
        task = self.get_task(task_id)
        if task is None:
            raise TaskIdNotFoundError
        for subtask in self.tasks:
            if subtask.parent_id == task.id:
                subtask.parent_id = task.parent_id
        self.tasks.remove(task)
        self.save()
        return task

    def list_tasks_parent(self, parent_id) -> List[Task]:
        return [t for t in self.tasks if t.parent_id == parent_id]

    def list_tasks(self) -> List[Task]:
        return self.tasks

    def list_subtasks(self, parent_id: UUID):
        return [t for t in self.tasks if t.parent_id == parent_id]

    def list_completed(self) -> List[Task]:
        return [task for task in self.tasks if task.done]

    def list_uncompleted(self) -> List[Task]:
        return [task for task in self.tasks if not task.done]
