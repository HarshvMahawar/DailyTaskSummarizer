import json
import os.path
import time

from path import abs_path


def setup_gmail():
    """
    Set up the Gmail address used for authenticating the application.

    If the Gmail address is already set, the user is prompted to update it.
    """
    if os.path.exists(abs_path("gmail.json")):
        update = input("Gmail is already set, do you want to update it? (Y/N)")
        if update != "Y":
            return None
    else:
        print("Gmail not set, proceeding to set up...")
    time.sleep(1)
    gmail = input("Enter the Gmail address used for authenticating the app:\n")
    with open(abs_path("gmail.json"), "w") as gmail_address:
        json.dump({"gmail": gmail}, gmail_address)
        print("Successfully set your Gmail address!")


if __name__ == "__main__":
    setup_gmail()
