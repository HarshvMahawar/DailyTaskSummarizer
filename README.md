# Daily Task Summarizer
## Introduction
Welcome to the Google Tasks Automation project! This Python-based automation tool is designed to simplify and streamline your task management on Google Tasks. Say goodbye to manual updates and hello to efficiency!

## What Does It Do?
Picture this: you wake up, grab your coffee, and wonder, "What did I conquer yesterday?" Enter the Task Wizard, your personal assistant powered by Python magic and the Google Tasks API.

### Step 1: Snatching Tasks
Every night, while you're peacefully dreaming of unicorns, the Task Wizard sneakily grabs all your Google Tasks from the previous day. It's like having a silent ninja tracking your accomplishments, incomplete missions, and even the tasks you decided to let go (we won't judge!).

### Step 2: Sorting the Magic Potions
Now, the Task Wizard concocts a detailed report, breaking down your tasks into categories:
🌟 Completed Tasks: Your victories! Celebrate the wins, big or small.
📅 Incomplete Tasks: The quests that will carry over to today. Don't worry; you've got this!
🚮 Deleted Tasks: The tasks that met their demise. Farewell, old tasks!

### Step 3: The Owl Post 🦉✉️
Hold on to your wizard hat because here comes the real magic! The Task Wizard, being the tech-savvy sorcerer it is, uses the Gmail API to send you a beautifully crafted email. Inside, you'll find your personalized task report, neatly organized and ready to guide your day.

## Getting Started
Follow these steps to set up the project and get it running in no time.

### Prerequisites

Make sure you have the following prerequisites installed:
* Python 3.10.7 or greater
* The pip package management tool
* A Google Cloud project ([Follow this link](https://developers.google.com/workspace/guides/create-project))
* A Google account with Google Tasks and Google Gmail APIs enabled

### Setting Up Your Environment
Follow the following steps:

1. **Enable the Google Tasks and Google Gmail API:**
* Go to the Google Cloud Console.
* Enable the Google Tasks and Google Gmail API ([Follow this link](https://console.cloud.google.com/flows/enableapi?apiid=tasks.googleapis.com))

2. **Configure the OAuth Consent Screen:**
* Navigate to Menu > APIs & Services > OAuth consent screen.
* Select the user type for your app and follow the on-screen instructions to complete the setup.
* Don't worry if it seems daunting; we're here to make it as painless as possible.

3. **Authorize Credentials for a Desktop Application:**
* Go to Menu > APIs & Services > Credentials.
* Create a new OAuth client ID for a Desktop app.
* **(Important)** Save the downloaded JSON file as credentials.json and move it to your working directory (where all your python scripts will be stored).

## Let's Delve into the coding part
Explore the Python scripts that house the enchanting logic of our Task Wizard.

First, let's make things a bit more easier! You have two ways to install the dependencies to get our Python scripts up and running:
1. Take it step by step and install the required libraries one by one.
2. Keep it super simple by downloading the requirements.txt file from the link at the end.
### authenticate.py
This script ensures that your Task Wizard is equipped with the necessary credentials to perform its magical tasks securely. Onward to the enchanted realms of automation!
🧙‍♂️✨
```python
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

```
#### Explanation:
*check_authentication Function:*
This function checks if the application is authenticated. If not, it prompts the user for authentication. If the user chooses to authenticate, it calls the authenticate function.

*authenticate Function:*
This function performs a one-time authentication process using OAuth. It checks if the app is already authenticated, and if not, it initiates the authentication flow. The user's access and refresh tokens are stored in the token.json file for future use.

*abs_path Function:*
The abs_path function, mentioned but not explained yet, will be clarified later in the documentation. For now assume that it just formats the path of particular file.

### client.py
Now that our Task Wizard has its credentials sorted out, it's time to forge the mystical connection between the server and the client.
```python
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
```
#### Explanation:
*set_up_creds Function:*
This function serves as the backstage manager, ensuring everything is in order before the Task Wizard's performance:
1. Check Authentication:
Verifies if the user is authenticated by calling the check_authentication function. If not, it prompts the user to authenticate.
2. Load Credentials:
Loads and creates credentials from the token.json file, essentially preparing the Task Wizard's identification papers for the Google APIs.

*client Function:*
This function sets up the connection between the server and client, guiding the Task Wizard through the intricacies of the Google APIs:
1. Get Credentials:
Calls set_up_creds to fetch the necessary credentials.
2. API Connection Forged:
Attempts to build the Google Tasks or Gmail API service using the build method, with the api parameter determining the chosen path.

### default_tasklist.py
The default_tasklist.py script takes charge of setting up the tasklist that our project will fetch to create the tasks report.
```python
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
```
#### Explanation
*default_tasklist Function:*
This function acts as the tasklist conductor, orchestrating the creation of the default tasklist:

1. Check Default Tasklist:
Examines if a default tasklist already exists. If so, it prompts the user to decide whether to set a new tasklist as default.
2. Create New Default Tasklist:
If no default tasklist exists or the user opts for a new one, initiates the creation process and safeguards the details in 'default_tasklist.json'.

*new_default_tasklist Function:*
This function is the architect of the new default tasklist, ensuring a seamless creation process:

1. Google Tasks API Client:
Creates a client for the Google Tasks API using the client function from the client.py module.
2. User Input:
Requests the user to provide a title for the new tasklist.
3. Tasklist Creation:
Communicates with the Google Tasks API to insert a new tasklist with the provided title.
4. Details Storage:
Records the details of the freshly crafted tasklist in 'default_tasklist.json'.

 ### gmail.py
 The gmail.py script is your gateway to configuring the Gmail address crucial for authenticating the application and sending the task reports. 
```python
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
```
#### Explanation
*setup_gmail Function:*
This function is the architect of your Gmail configuration, ensuring a seamless setup:

1. Check Existing Gmail:
Checks if a Gmail address is already configured. If it is, prompts the user to decide whether to update it.
2. Gmail Setup Process:
If no Gmail address is configured or the user opts for an update, initiates the setup process.
3. User Input:
Asks the user to input the Gmail address to be used for authenticating the app and sending the report through mail.
4. Details Storage:
Records the Gmail address details in 'gmail.json'.

### tasks.py
The tasks.py script fetches task details from the default tasks list of the previous day and crafts a detailed report using the gathered data.
```python
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
```
#### Explanation:
*date_today Function:*
Fetches the current date.

*date_tomorrow Function:*
Fetches the date for tomorrow.

*get_df_tasklist_id Function:*
Retrieves the ID of the default tasklist from 'default_tasklist.json'.

*list_tasks Function:*
Lists tasks for the current day using the Google Tasks API.

*TaskReportGenerator Class:*

1. __init__ Method:
Initializes the TaskReportGenerator class with task data.
2. generate_report Method:
Crafts a detailed report of completed, deleted, and pending tasks. Feel free to customize the report's content to match what inspires you the most! :)

### mail_report.py
The mail_report.py script is the mystical messenger that sends the crafted task report to the user's Gmail address.
```python
import base64
import json
import os
from email.mime.text import MIMEText

from client import client  # Import the 'client' function from a custom module
from gmail import setup_gmail  # Import the 'setup_gmail' function from a custom module
from googleapiclient import errors
from path import abs_path
from tasks import TaskReportGenerator, list_tasks  # Import custom modules


def send_message(api_client, message):
    """
    Send an email message using the Gmail API.

    Args:
        api_client (googleapiclient.discovery.Resource): The Gmail API client.
        message (dict): The message to be sent.

    Returns:
        dict: The sent message details.
    """
    message = api_client.users().messages().send(userId="me", body=message).execute()
    return message


def create_message(sender, to, subject, message_text):
    """
    Create an email message.

    Args:
        sender (str): The email address of the sender.
        to (str): The email address of the recipient.
        subject (str): The email subject.
        message_text (str): The email message content.

    Returns:
        dict: The email message in a format suitable for sending.
    """
    message = MIMEText(message_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    return {"raw": base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def main():
    try:
        if not os.path.exists(abs_path("gmail.json")):
            setup_gmail()  # Set up the Gmail address if not already set
        with open(abs_path("gmail.json"), "r") as mail:
            user_gmail = json.load(mail)["gmail"]
        api_client = client("gmail")  # Create a Gmail API client
        tasks_list = list_tasks()  # Get the list of tasks
        report_generator = TaskReportGenerator(tasks_data=tasks_list)
        tasks_report = (
            report_generator.generate_report()
        )  # Generate a report from tasks
        email = create_message(
            user_gmail, user_gmail, "Daily task-bot report!", tasks_report
        )
        email_sent = send_message(api_client, email)  # Send the email
        print("Message Id:", email_sent["id"])
    except errors.HttpError as e:
        print(e)


if __name__ == "__main__":
    main()  # Run the main function when the script is executed
```
#### Explanation:
*send_message Function:*
Sends an email message using the Gmail API.

*create_message Function:*
Creates an email message in a format suitable for sending.

*main Function:*
Orchestrates the entire process of sending the task report via email.

### path.py
Lets also understand what the abs_path function do. It ensures that you get the absolute path of a file by combining the directory of the current script with the provided file name.

In simpler terms, when you run the mail_report.py script from a different directory, the abs_path function ensures that the script looks for the gmail.json file in the correct location. Without abs_path, the script might incorrectly search for gmail.json in the directory from which the script is executed. abs_path adjusts the search path to the correct project directory.

```python
import os.path


def abs_path(file_name):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, file_name)
    return file_path
```
#### Explanation:
*abs_path Function:*
This is useful for creating a reliable and portable file path, especially when dealing with file operations in a script that may be executed from different locations.

1. os.path.abspath(__file__):
Retrieves the absolute path of the current script file (__file__ contains the path of the current Python script).
2. os.path.dirname(...):
Extracts the directory portion of the absolute path obtained in the previous step.
3. os.path.join(...):
Joins the directory path with the provided file name to create the complete file path.

## Now that you have your scripts ready, let's weave the magic and set up your Task Wizard step by step.


1. **Download `credentials.json`:**
   - If you haven't done so already, follow the earlier instructions to download your `credentials.json` file from the Google Cloud Console.

2. **Authenticate the App:**
   - Run the `authenticate.py` script to initiate the authentication process.
   - This magical script will create the essential `token.json` file using your `credentials.json`.

3. **Set Up Default Tasklist:**
   - Execute the `default_tasklist.py` script to establish your default tasklist.
   - If you ever want to switch to a new one, this script has got you covered.

4. **Set Up Gmail:**
   - Run the `gmail.py` script to set up the Gmail address used for authentication.
   - Make sure your Task Wizard knows where to send the daily reports.

5. **Mail Your Report:**
   - Ready for the enchantment? Execute the `mail_report.py` script to send your personalized task report.
   - Customize the script, make it your own, and share the magic!

6. **Automation (Optional, but Magical):**
   - Want the Task Wizard to work its magic automatically? Consider setting up the entire project on a cloud server.
   - Utilize cron jobs or other scheduling methods to automate the `mail_report.py` script.
   - Now, your Task Wizard will send you daily reports like clockwork!

Feel the magic, customize your journey, and let the Task Wizard make your daily tasks enchanting! ✨📜✉️

### Your valuable contributions are warmly welcomed
