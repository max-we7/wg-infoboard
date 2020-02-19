import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


def init_google_sheet():
    """
    initializes connection to Google Sheets
    :return: returns a sheet instance that can be used to call functions on
    """
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_sheets_creds.json", scope)
    client = gspread.authorize(creds)
    return client.open("finances").sheet1


def get_balances():
    """
    returns list of balances for all users
    """
    sheet = init_google_sheet()
    balances_raw = [[name, sheet.cell(3, i).value] for name, i in [("Max", 7), ("Noah", 8), ("Nawid", 9), ("Seb", 10)]]
    balances = {
        "Max": int(balances_raw[0][1].replace(',', '')[:-2]),
        "Nawid": int(balances_raw[1][1].replace(',', '')[:-2]),
        "Noah": int(balances_raw[2][1].replace(',', '')[:-2]),
        "Seb": int(balances_raw[3][1].replace(',', '')[:-2])
    }
    now = datetime.now()
    date = now.strftime("%d.%m.%Y")
    return balances, date


def get_balances_raw():
    """
    returns list of balances for all users
    """
    sheet = init_google_sheet()
    return [[name, sheet.cell(3, i).value] for name, i in [("Max", 7), ("Noah", 8), ("Nawid", 9), ("Seb", 10)]]


def get_history():
    """
    returns the three most recent transactions
    """
    sheet = init_google_sheet()
    history = []
    for row in [3, 4, 5]:
        history.append([sheet.cell(row, i).value for i in range(11) if i != 0])
    return history


def add_entry(new_row):
    """
    adds a given row to the top of the spreadsheet, automatically pushing down all rows beneath
    :param new_row: takes an array of new entries as an argument
    """
    sheet = init_google_sheet()
    sheet.insert_row(new_row, 3)


def delete_entry():
    sheet = init_google_sheet()
    sheet.delete_row(3)
