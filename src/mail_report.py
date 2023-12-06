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
