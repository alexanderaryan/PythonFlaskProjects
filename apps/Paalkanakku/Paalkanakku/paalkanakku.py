from Paalkanakku.Paalkanakku import gspread
from Paalkanakku.Paalkanakku import cred_filename, gcc
from Paalkanakku.Paalkanakku.config import book_name, sheet_name

#print (gcc.openall())

try:
    workbook = gcc.open(book_name)
except gspread.exceptions.SpreadsheetNotFound as e:
    print(f"{book_name} not found in your Google Drive. Creating one!")
    workbook = gcc.create(book_name)
else:
    print(f"Successfully opened Spreadsheet: {book_name}")


try:
    sheet = workbook.worksheet(sheet_name)
except gspread.exceptions.WorksheetNotFound as e:
    sheet = workbook.add_worksheet(sheet_name, rows=1000, cols=1000)
    print(f"{sheet_name} not found in your {book_name}. Created one!")
else:
    print(f"Successfully opened Worksheet: {sheet_name}")





