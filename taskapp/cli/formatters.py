from taskapp.tasks import Task, TaskManager

def format_task(task: Task) -> str:
    status = "✔" if task.done else " "
    return f"- [{status}] {task.title}"