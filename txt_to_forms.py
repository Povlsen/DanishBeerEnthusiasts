#!/usr/bin/env python
import os
import argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Parse command-line arguments: the input file (e.g., beers.txt)
parser = argparse.ArgumentParser(
    description="Create a Google Form from a text file where each line becomes a question."
)
parser.add_argument(
    "input_file", 
    help="Path to the input file (e.g., beers.txt) containing the questions."
)
args = parser.parse_args()

# Use the file name (without extension) as the form title.
form_title = os.path.splitext(os.path.basename(args.input_file))[0]

# Hardcoded personal email address to share the form with.
USER_EMAIL = "nikolaipovlsen@yahoo.dk"  # Replace with your email

# Path to your service account JSON credentials.
SERVICE_ACCOUNT_FILE = r'C:\Users\nikol\DØE\artful-mystery-451710-n5-eff4f2994ffa.json'

# Scopes needed for managing Google Forms and for Drive file updates/sharing.
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/drive'
]

# Authenticate using the service account.
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Build the Google Forms and Drive API services.
forms_service = build('forms', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

# Create a new form with the title derived from the file name.
new_form = {
    "info": {
        "title": form_title
    }
}
create_response = forms_service.forms().create(body=new_form).execute()
form_id = create_response['formId']
print(f"Created form with ID: {form_id}")

# Update the file name in Drive to match the form title.
drive_service.files().update(
    fileId=form_id,
    body={"name": form_title}
).execute()
print(f"File name updated to: {form_title}")

# Read the file and get non-empty lines.
with open(args.input_file, 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

# Prepare a batchUpdate request: each line becomes a question with radio button choices 1–10.
requests = []
for index, line in enumerate(lines):
    question_request = {
        "createItem": {
            "item": {
                "title": line,
                "questionItem": {
                    "question": {
                        "choiceQuestion": {
                            "type": "RADIO",
                            "options": [{"value": str(i)} for i in range(1, 11)],
                            "shuffle": False
                        }
                    }
                }
            },
            "location": {
                "index": index
            }
        }
    }
    requests.append(question_request)

batch_update_request = {"requests": requests}
forms_service.forms().batchUpdate(formId=form_id, body=batch_update_request).execute()
print("Form updated with questions.")

# Share the form with your hardcoded email so you can see it in your Drive.
permission = {
    'type': 'user',
    'role': 'writer',  # Use 'reader' for view-only access if desired.
    'emailAddress': USER_EMAIL
}
drive_service.permissions().create(
    fileId=form_id,
    body=permission,
    fields='id'
).execute()
print(f"Form shared with {USER_EMAIL}.")

# Print the edit URL so you can open the form in edit mode.
edit_url = f"https://docs.google.com/forms/d/{form_id}/edit"
print("Access your form (edit mode) at:", edit_url)
