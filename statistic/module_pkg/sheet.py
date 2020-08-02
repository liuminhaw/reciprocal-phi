# -*- conding: UTF-8 -*-


# Third party library imports
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request 


class StatsSheet():

    def __init__(self, credential, spreadsheet_id):
        """
        Input params:
            credential - Credential to use Google sheet API
            spreadsheet_id - target spreadsheet id
        """
        self.service = build('sheets', 'v4', credentials=credential)
        self.id = spreadsheet_id

    def create_new_sheet(self, title, sheet_id=None, index=0):
        batch_update_spreadsheet_request_body = {
            'requests': [
                {
                    'addSheet': {
                        'properties': {
                            'sheetId': sheet_id,
                            'title': title,
                            'index': index
                        }
                    }
                },
                {
                    "mergeCells": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 2
                        },
                        "mergeType": "MERGE_ROWS"
                    }
                },
                {
                    "mergeCells": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                            "startColumnIndex": 2,
                            "endColumnIndex": 4
                        },
                        "mergeType": "MERGE_ROWS"
                    }
                }
            ]  
        }

        request = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.id, body=batch_update_spreadsheet_request_body
            ).execute()


    def statistic_write(self, range, data):
        """
        Write statistic data to sheet
        Inputs:
            data - array list data for writing to sheet
        """
        batch_update_values_request_body = {
            # How the input data should be interpreted.
            'value_input_option': 'RAW',
            'data': [
                {
                    'range': range,
                    'majorDimension': 'ROWS',
                    'values': data
                }
            ]  
        }

        self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.id, body=batch_update_values_request_body
            ).execute()



def statistic_to_data(statistic):
    """
    Turn statistic dict data into array list for Google sheet import 
    """
    sheet_data = []

    for key, value in statistic.items():
        row_data = [str(key), value]
        sheet_data.append(row_data)
    sheet_data.sort()

    return sheet_data