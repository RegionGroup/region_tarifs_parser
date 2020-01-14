import time
import datetime
import platform

import gspread

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Gdoc(object):

    def __init__(self, path_to_cred):
        self.path_to_cred = path_to_cred

    def g_sheets_update(self, parser ,doc_id, clear_status=True):
        # row coll
        cell = ''
        # Авторизация и загрузка документа
        scope = ['https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.path_to_cred, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(doc_id).sheet1

        # Проверка есть ли в документе такой конкурент
        try:
            cell = sheet.find(parser.get_name())
            start_row = cell.row
        except Exception as e:
            start_row = len(sheet.col_values(1))+1

        # Проверка даты
        date_now = str(datetime.date.today())
        all_dates = sheet.row_values(1)
        start_coll = len(sheet.row_values(1))
        if all_dates[-1] == date_now:
            pass
        else:
            start_coll += 1
        sheet.update_cell(1,start_coll, date_now)

        # Запись данных | row coll
        for tarif in parser.get_tarifs():
            
            try:
                title = tarif['title']
            except Exception as e:
                title = ''

            try:
                speed = tarif['speed']
            except Exception as e:
                speed = ''
            
            try:
                if clear_status:
                    price = tarif['price']
                else:
                    price = tarif['price']
            except Exception as e:
                price = ''

            cell = '''{}\n{}\n{}'''.format(title, speed, price).strip()

            sheet.update_cell(start_row, start_coll, cell)
            sheet.update_cell(start_row, 1, parser.get_name())
            time.sleep(15)
            start_row += 1

    def g_sheets_errorlog(self, errors, doc_id):
        # row coll
        cell = ''
        # Авторизация и загрузка документа
        scope = ['https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.path_to_cred, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(doc_id).get_worksheet(1)
        data = sheet.get_all_records()

        start_row = len(sheet.col_values(1))+1

        # Проверка даты
        date_now = str(datetime.date.today())
        all_dates = sheet.row_values(1)
        start_coll = len(sheet.row_values(1))
        if all_dates[-1] == date_now:
            pass
        else:
            start_coll += 1
        sheet.update_cell(1,start_coll, date_now)

        val = sheet.cell(start_row, start_coll).value
        while val:
            start_row += 1
            val = sheet.cell(start_row, start_coll).value
        
        # Запись данных | row coll
        for error in errors:
            cell = error
            sheet.update_cell(start_row, start_coll, cell)
            start_row += 1

    def add_colums(self, doc_id):
        scope = ['https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.path_to_cred, scope)
        client = gspread.authorize(creds)
        sheet_main = client.open_by_key(doc_id).sheet1
        sheet_error = client.open_by_key(doc_id).get_worksheet(1)
        sheet_main.add_cols(1)
        sheet_error.add_cols(1)