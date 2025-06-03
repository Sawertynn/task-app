from taskapp.tasks import TaskManager
from taskapp.cli import format_task

def main():
    print(" === Task App CLI === ")
    manager = TaskManager()
    manager.add_new_task('first task')
    manager.add_new_task('secnd task')
    manager.list_tasks()[1].finish()
    for task in manager.list_tasks():
        print(format_task(task))


if __name__ == "__main__":
    main()
