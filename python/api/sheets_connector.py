import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from python.main.config import wg_members


def init_google_sheet():
    """
    initializes connection to Google Sheets
    :return: returns a sheet instance that can be used to call functions on
    """
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    print("3")
    print(os.getcwd())
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("../api/google_sheets_creds.json", scope)
    except Exception as e:
        print(e)
    print("4")
    client = gspread.authorize(creds)
    print("5")
    return client.open("finances").sheet1


def get_balances():
    """
    returns list of balances for all users
    """
    sheet = init_google_sheet()
    balances_raw = [sheet.cell(3, i).value for i in [7, 8, 9, 10]]
    balances = {}
    for i in range(4):
        balances.update({wg_members[i]: int(balances_raw[i].replace(',', '')[:-2])})
    return balances


def get_balances_raw():
    """
    returns list of balances for all users
    """
    print("2")
    sheet = init_google_sheet()
    return [[name, sheet.cell(3, i).value] for name, i in [(wg_members[0], 7), (wg_members[1], 8),
                                                           (wg_members[2], 9), (wg_members[3], 10)]]


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
    """
    delete the most recently added entry
    """
    sheet = init_google_sheet()
    sheet.delete_row(3)
