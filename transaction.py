# This file will define functions for operating transactions

from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd

class Transaction:
    def import_csv(self):
        # hide the main window
        Tk().withdraw()

        # choose a file
        file_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
        print("Load file successfully:", file_path)

        # read the csv file
        df = pd.read_csv(file_path)
        df["Date"] = pd.to_datetime(df["Date"])
        return df

    def view_transaction(self, df):
        print("View transaction")
        print(df)

    def view_transactions_filter(self, df):
        print("View transactions by date range, category, type")

    def add_transaction(self):
        print("Add transactions")
        return []

    def edit_transaction(self, df):
        print("Edit transactions")
        return []

    def delete_transaction(self, df):
        print("Delete transactions")
        return []

    def set_income(self):
        print("Set income")
        return []

    def save_csv(self, df):
        print("Save csv")

    def exit(self):
        print("Exit")