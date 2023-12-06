from __future__ import print_function

import os.path
import time

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from path import abs_path

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/tasks", "https://mail.google.com/"]


def check_authentication():
    """
    Check if the application is authenticated. If not, prompt the user for authentication.

    If not authenticated, the user is given the option to initiate the authentication process.
    """
    # If the tool is not authenticated
    if not os.path.exists(abs_path("token.json")):
        time.sleep(0.2)
        do_auth = input(
            "App is not authenticated, do you want to authenticate now? (Y/N)"
        )
        time.sleep(0.5)
        if do_auth == "Y":
            authenticate()
        else:
            print("App is not yet authenticated, Please refer to Readme.md")
            return None


def authenticate():
    """
    Perform a one-time authentication process to set up the 'token.json' file.
    """
    creds = None
    # The file 'token.json' stores the user's access and refresh tokens and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(abs_path("token.json")):
        print("App is already authenticated!")
        return None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                abs_path("credentials.json"), SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(abs_path("token.json"), "w") as token:
            token.write(creds.to_json())


if __name__ == "__main__":
    authenticate()
