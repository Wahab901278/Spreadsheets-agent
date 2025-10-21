Google Cloud Account Setup Guide

Complete Steps to Connect Google Cloud Account for Sheets API Integration

Step 1: Create a Google Cloud Project

1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Click on the project dropdown at the top
3. Click "New Project"
4. Enter project name: "Spreadsheet-Analysis-Agent"
5. Click "Create"
6. Wait for project creation to complete

Step 2: Enable Google Sheets API

1. In the Google Cloud Console, search for "Google Sheets API"
2. Click on "Google Sheets API" from the search results
3. Click the "Enable" button
4. This enables the API for your project

Step 3: Create a Service Account

1. In the Google Cloud Console, go to "APIs & Services" > "Credentials"
2. Click "+ Create Credentials"
3. Select "Service Account"
4. Fill in the details:
   - Service account name: "spreadsheet-agent"
   - Service account ID: (auto-filled)
   - Description: "Service account for spreadsheet analysis"
5. Click "Create and Continue"
6. For "Grant this service account access to project":
   - Select role: "Editor" (or "Viewer" if read-only is sufficient)
7. Click "Continue"
8. Click "Done"

Step 4: Create a Service Account Key

1. In the Google Cloud Console, go to "APIs & Services" > "Service Accounts"
2. Click on the service account you just created
3. Go to the "Keys" tab
4. Click "Add Key" > "Create new key"
5. Choose "JSON" format
6. Click "Create"
7. The JSON file will be automatically downloaded

Step 5: Set Up Local Project with Service Account Key

1. In your project root directory, create a folder:
   mkdir crediantials

2. Move the downloaded JSON file:
   mv ~/Downloads/[service-account-name]-*.json crediantials/service_account.json

3. Add the credentials folder to .gitignore:
   echo "crediantials/" >> .gitignore

Step 6: Share Your Google Sheet with Service Account

1. Open your Google Sheet
2. Click "Share" in the top right
3. In the JSON file you downloaded, find the "client_email" field
4. It looks like: spreadsheet-agent@[project-id].iam.gserviceaccount.com
5. Paste this email into the share dialog
6. Give it "Editor" access (or "Viewer" if read-only)
7. Click "Share"

Step 7: Get Your Spreadsheet ID

1. Open your Google Sheet in a browser
2. Look at the URL: https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
3. Copy the SPREADSHEET_ID part (the long alphanumeric string)

Step 8: Configure .env File

1. Copy the example file:
   cp .env.example .env

2. Edit .env and add your values:

   SPREADSHEET_ID=your_spreadsheet_id_here
   READ_RANGE=Sheet1!A1:Z1000
   WRITE_RANGE=Sheet1!AB1
   GOOGLE_SERVICE_ACCOUNT_JSON=crediantials/service_account.json
   LLM_MODEL=llama2
   OLLAMA_BASE_URL=http://localhost:11434

3. Replace:
   - your_spreadsheet_id_here with the ID from Step 7
   - Sheet1 with your actual sheet name if different
   - A1:Z1000 with your data range if different

Step 9: Test the Connection

1. Install dependencies:
   pip install -r requirements.txt

2. Run a quick test:
   python main.py

3. You should see logs showing successful connection to Google Sheets

Step 10: Troubleshooting

Issue: "FileNotFoundError: Google service account file not found"
Solution:
- Check that crediantials/service_account.json exists
- Verify the path in .env is correct
- Make sure the file is in the right location

Issue: "403 Forbidden" error
Solution:
- Ensure you've enabled Google Sheets API in Google Cloud Console
- Verify you've shared the Google Sheet with the service account email
- Check that the service account has Editor role

Issue: "404 Not found" error for spreadsheet
Solution:
- Verify SPREADSHEET_ID is correct
- Ensure the sheet exists and is accessible
- Check that service account has access to the sheet

Issue: "Invalid range" error
Solution:
- Verify READ_RANGE syntax: Sheet1!A1:Z1000
- Check sheet names don't have spaces (or use single quotes: 'Sheet Name'!A1:Z10)
- Ensure rows and columns exist in your sheet

Important Security Notes

1. Never commit service_account.json to version control
2. Keep the JSON file secure and private
3. Rotate service account keys periodically
4. Don't hardcode credentials in code
5. Use environment variables for sensitive data
6. Review Google Cloud Console regularly for suspicious activity

Additional Resources

- Google Sheets API Documentation: https://developers.google.com/sheets/api
- Service Account Documentation: https://cloud.google.com/iam/docs/service-accounts
- Google Cloud Console: https://console.cloud.google.com/
- Python Google API Client: https://github.com/googleapis/google-api-python-client

Common Issues and Solutions

Managing Multiple Spreadsheets

To work with different spreadsheets, create different .env configurations:

.env.production
SPREADSHEET_ID=production_sheet_id
READ_RANGE=Sheet1!A1:Z1000

.env.testing
SPREADSHEET_ID=testing_sheet_id
READ_RANGE=TestData!A1:Z1000

Load them:
from dotenv import load_dotenv
load_dotenv('.env.production')

API Rate Limits

Google Sheets API has rate limits:
- Reads: 300 requests per minute per user
- Writes: 60 requests per minute per user

For large operations, implement delays:

import time
for sheet_id in sheet_ids:
    read_sheet(sheet_id)
    time.sleep(1)  # Wait 1 second between requests

Revoking Access

If you need to revoke service account access:

1. Go to Google Cloud Console
2. Go to "APIs & Services" > "Service Accounts"
3. Click on the service account
4. Click the "Delete" button
5. Unshare the Google Sheet from the service account email

Complete Example Workflow

1. Create project in Google Cloud
2. Enable Sheets API
3. Create service account and download key
4. Save key to crediantials/service_account.json
5. Share Google Sheet with service account email
6. Get spreadsheet ID from sheet URL
7. Configure .env file
8. Run: python main.py
9. Check logs for successful execution

The workflow is now connected to your Google Sheets account!
