
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def save_to_sheet(data):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Buyurtmalar").sheet1
    sheet.append_row([data["date"], data["name"], data["service"], data["phone"], data["note"]])
