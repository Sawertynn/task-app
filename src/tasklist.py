from task import Task


class TaskList:
    def __init__(self):
        self.tasks: list[Task] = []

    def add_new_task(self, text):
        task = Task(text)
        self.tasks.append(task)

    def print_all_tasks(self):
        for pos, task in enumerate(self.tasks):
            print(pos, task)

    def print_unfinished(self):
        for pos, task in enumerate(self.tasks):
            if not task.is_finished():
                print(pos, task)
