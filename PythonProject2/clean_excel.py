import xlwings as xw
import pandas as pd

def clean_data():
    wb = xw.Book.caller()   # Connects to the Excel workbook
    sheet = wb.sheets[0]    # First sheet

    # Read data from Excel into pandas dataframe
    df = sheet.range("A1").options(pd.DataFrame, header=1, index=False).value

    # Example cleaning: drop missing values
    df = df.dropna()

    # Write cleaned data back into Excel (starting at column E1)
    sheet.range("E1").value = df
