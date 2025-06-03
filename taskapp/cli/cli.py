import argparse

from taskapp.tasks import TaskManager
from taskapp.cli.formatters import print_task_tree
from taskapp.storage.filedb import FileDB

path = "data/tasks.json"

def main():
    print(" === Task App CLI === ")
    parser = argparse.ArgumentParser("Task-App CLI")
    parser.add_argument("-a", "--add", help="Add a task")
    parser.add_argument("-u", "--under", help="Parent task ID (for --add)", default=None)
    parser.add_argument("-l", "--list", action="store_true", help="List tasks")
    parser.add_argument("-c", "--checkoff", help="Check off the task, mark as done")
    parser.add_argument("-d", "--delete", help="Delete the task entirely")
    args = parser.parse_args()

    filedb = FileDB(path)
    manager = TaskManager(filedb)

    if args.add:
        task = manager.add_task(args.add, parent_id=args.under)
        print(f"Added task: {task.title} [{task.id}] (under {args.under or 'root'})")

    if args.checkoff:
        task = manager.mark_done(args.checkoff)
        print(f"Checked done: {task.title} [{task.id}]")

    if args.delete:
        task = manager.delete(args.delete)
        print(f"Deleted: {task.title} [{task.id}]")

    if args.list:
        print_task_tree(manager)


if __name__ == "__main__":
    main()
