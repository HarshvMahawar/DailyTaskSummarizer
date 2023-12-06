import datetime
import json

import rfc3339
from client import client  # Import the 'client' function from a custom module
from path import abs_path


def date_today():
    """
    Get the current date.

    Returns:
        datetime.date: The current date.
    """
    date_today = datetime.date.today()
    return date_today


def date_tomorrow():
    """
    Get the date for tomorrow.

    Returns:
        datetime.date: The date for tomorrow.
    """
    date_tomorrow = date_today() + datetime.timedelta(days=1)
    return date_tomorrow


def get_df_tasklist_id():
    """
    Get the ID of the default tasklist.

    Returns:
        str: The ID of the default tasklist.
    """
    with open(abs_path("default_tasklist.json"), "r") as df_tasklist:
        default_tasklist = json.load(df_tasklist)
        return default_tasklist["id"]


def list_tasks():
    """
    List tasks for the current day.

    Returns:
        dict: The list of tasks for the current day.
    """
    api_client = client("tasks")
    tasks = (
        api_client.tasks()
        .list(
            tasklist=get_df_tasklist_id(),
            dueMax=rfc3339.rfc3339(date_tomorrow()),
            dueMin=rfc3339.rfc3339(date_today()),
            showCompleted=True,
            showHidden=True,
            showDeleted=True,
        )
        .execute()
    )
    return tasks


class TaskReportGenerator:
    def __init__(self, tasks_data):
        self.tasks_data = tasks_data

    def generate_report(self):
        """
        Generate a report of completed, deleted, and pending tasks.

        Returns:
            str: The generated task report.
        """
        completed_tasks = [
            task for task in self.tasks_data["items"] if task["status"] == "completed"
        ]
        deleted_tasks = [
            task for task in self.tasks_data["items"] if task.get("deleted", False)
        ]
        pending_tasks = [
            task for task in self.tasks_data["items"] if task["status"] == "needsAction"
        ]

        report = (
            f"Hi! Daily task-bot here, given below is the task report of yesterday:\n\n"
        )

        # Completed Tasks
        if completed_tasks:
            report += f"Completed Tasks ({len(completed_tasks)}):\n"
            for task in completed_tasks:
                report += f"- {task['title']} (Completed on {task['completed']} UTC)\n"
            report += "\n"

        # Deleted Tasks
        if deleted_tasks:
            report += f"Deleted Tasks ({len(deleted_tasks)}):\n"
            for task in deleted_tasks:
                report += f"- {task['title']} (Deleted on {task['updated']} UTC)\n"
            report += "\n"

        # Pending Tasks
        if pending_tasks:
            report += f"Pending Tasks ({len(pending_tasks)}):\n"
            for task in pending_tasks:
                report += f"- {task['title']}\n"
        if (
            report
            == "Hi! Daily task-bot here, given below is the task report of yesterday:\n\n"
        ):
            report += "Oops! NO tasks to mention!"
        return report