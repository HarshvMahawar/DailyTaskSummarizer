from __future__ import print_function

# Import necessary modules
from authenticate import check_authentication
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from path import abs_path

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/tasks", "https://mail.google.com/"]


def set_up_creds():
    """
    Set up Google API credentials by checking authentication and loading them from a 'token.json' file.

    Returns:
        google.oauth2.credentials.Credentials: The Google API credentials object.
    """
    check_authentication()  # Check if the user is authenticated
    creds = Credentials.from_authorized_user_file(
        abs_path("token.json"), SCOPES
    )  # Load and create credentials from the 'token.json' file
    return creds  # Return the credentials


def client(api):
    """
    Create a Google API client using an existing token.json file.

    Args:
        api (str): The API to create a client for, should be 'tasks' or 'gmail'.

    Returns:
        googleapiclient.discovery.Resource: The Google API client resource.

    Raises:
        Exception: If an error occurs during the client creation.
    """
    creds = set_up_creds()  # Get the credentials

    try:
        # Build the Google Tasks API service or Gmail API service based on the 'api' parameter
        service = build(
            api, "v1", credentials=creds
        )  # Create a Google API client service
        return service  # Return the created API client service
    except Exception as e:
        print(
            f"An error occurred: {e}"
        )  # Handle exceptions and print an error message if one occurs
