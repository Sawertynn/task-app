from typing import Optional, List

from taskapp.tasks.task import Task


class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_new_task(self, title):
        task = Task(title)
        self.tasks.append(task)

    def get_task(self, task_id) -> Optional[Task]:
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None
    
    def list_tasks(self) -> List[Task]:
        return self.tasks
    
    def list_completed(self) -> List[Task]:
        return [task for task in self.tasks if task.done]
    
    def list_uncompleted(self) -> List[Task]:
        return [task for task in self.tasks if not task.done]
