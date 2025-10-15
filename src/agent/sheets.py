import os

from dataclasses import dataclass

from google.oauth2 import service_account
from googleapiclient.discovery import build


SCOPES=['https://www.googleapis.com/auth/spreadsheets']

@dataclass
class SheetsConfig:
    spreadsheet_id:str
    read_range:str
    write_range:str
    service_account_json:str="crediantials/service_account.json"

def get_sheets_service(service_account_json):
    json_path=service_account_json or os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON","crediantials/service_account.json")

    if not os.path.exists(json_path):
        raise FileNotFoundError(
            f"Google service account file not found at {json_path}"
        )
    creds=service_account.Credentials.from_service_account_file(json_path,scopes=SCOPES)
    service=build("sheets","v4",credentials=creds)

    return service.spreadsheets()
    

def read_sheet(config: SheetsConfig):
    sheets=get_sheets_service(config.service_account_json)
    result=result = (
        sheets.values()
        .get(spreadsheetId=config.spreadsheet_id, range=config.read_range)
        .execute()
    )
    values = result.get("values", [])
    return values


