import json
import os.path
import time

from client import client  # Import the 'client' function from a custom module
from path import abs_path


def default_tasklist():
    """
    Check if a default tasklist exists, and create one if it doesn't.

    If a default tasklist already exists, the user is prompted to create a new one.
    """
    if os.path.exists(abs_path("default_tasklist.json")):
        create_new = input(
            "Default Tasklist is already present, do you want to set a new tasklist as default? (Y/N)"
        )
        time.sleep(0.5)
        if create_new != "Y":
            return None
    else:
        print("No default tasklist, proceeding to create a new...")
    time.sleep(1)
    new_default_tasklist()


def new_default_tasklist():
    """
    Create a new default tasklist and store its details in 'default_tasklist.json'.
    """
    api_client = client("tasks")  # Create a Google Tasks API client
    tl_title = input("Enter the title of the new tasklist\n")
    response = api_client.tasklists().insert(body={"title": tl_title}).execute()
    with open(abs_path("default_tasklist.json"), "w") as df_tasklist:
        json.dump(response, df_tasklist)
        print("Successfully created a new default tasklist!")


if __name__ == "__main__":
    default_tasklist()
