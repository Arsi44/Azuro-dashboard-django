import os
import sqlite3

from dotenv import load_dotenv, find_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SQLConnecter():
    def __init__(self):
        self.sqlite_connection, self.cursor = self.connect_to_sqlite()

    def connect_to_sqlite(self):
        try:
            sqlite_connection = sqlite3.connect('../db.sqlite3')
            cursor = sqlite_connection.cursor()
            print("Successfully connected")

            return sqlite_connection, cursor

        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)

    def check_if_exists(self, participant_name: str) -> bool:
        query = """SELECT * FROM dashboard_dashboardrows WHERE participant_name = '{0}'""".format(
            participant_name)
        row = self.cursor.execute(query)
        if row.fetchone():
            return True
        else:
            return False

    def add_row(self, participant_name: str, points: str, cash: str):
        if points == '':
            points = '0'
        query = """INSERT INTO dashboard_dashboardrows (participant_name, points, cash)  VALUES  ('{0}', '{1}', '{2}')""".format(
            participant_name, points, cash)
        print(query)
        self.cursor.execute(query)
        self.sqlite_connection.commit()

    def update_row(self, participant_name: str, points: str, cash: str):
        if points == '':
            points = '0'
        query = """UPDATE dashboard_dashboardrows SET points = '{1}', cash = '{2}' WHERE participant_name = '{0}'""".format(
            participant_name, points, cash)

        self.cursor.execute(query)
        self.sqlite_connection.commit()

    def delete_row(self, participant_name: str):
        query = """DELETE FROM dashboard_dashboardrows WHERE participant_name = '{0}'""".format(
            participant_name)

        self.cursor.execute(query)
        self.sqlite_connection.commit()


def read_data():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    values = []
    try:
        service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=GOOGLE_TABLE_ID,
                                    range=CELLS_DIAPASON).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

    except HttpError as err:
        print(err)
    return values


# def write_data_in_db(data):
#     for row in data[1:]


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    GOOGLE_TABLE_ID = os.environ['GOOGLE_TABLE_ID']
    CELLS_DIAPASON = 'Sheet1!A1:C83'

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]  # Read only

    data = read_data()
    sgl_obj = SQLConnecter()


    for row in data[1:]:
        if sgl_obj.check_if_exists(row[0]):
            sgl_obj.update_row(row[0], row[1], row[2])
        else:
            sgl_obj.add_row(row[0], row[1], row[2])


