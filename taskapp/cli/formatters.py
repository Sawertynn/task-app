from taskapp.tasks import Task, TaskManager


def format_task(task: Task, depth=0):
    indent = "  " * depth
    status = "✔" if task.done else " "
    return f"{indent}- [{status}] {task.title} ({task.id})"


def print_task_tree(manager: TaskManager, parent_id=None, depth=0):
    tasks = manager.list_tasks_parent(parent_id)
    for task in tasks:
        print(format_task(task, depth))
        print_task_tree(manager, parent_id=task.id, depth=depth + 1)
