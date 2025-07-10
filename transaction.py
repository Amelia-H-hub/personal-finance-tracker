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

    def set_income(self, df):
        print("Set income")

        #  Get the date
        while True:
            try:
                date = pd.to_datetime(input("Enter the date (YYYY-MM-DD): "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid date.")
                continue
            except Exception:
                print("An unexpected error occurred.")
                continue

        #  Get a discription
        while True:
            try:
                desc = input("Enter a description: ")
                break
            except Exception:
                print("An unexpected error occurred.")
                continue
        
        #  Get the amount
        while True:
            try:
                amount = round(pd.to_numeric(input("Enter the amount: ")), 2)

                if amount > 0:
                    break
                else:
                    print("Invalid input. Please enter a value greater than 0.01.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            except Exception:
                print("An unexpected error occurred.")
                continue
        
        # Create a new row
        new_row = {
            "Date" : date,
            "Category" : "Income",
            "Description" : desc,
            "Amount" : amount,
            "Type" : "Income"
        }
        new_row_df = pd.DataFrame(new_row, index=[0])

        # Combine dataframe and a new row
        results_df = pd.concat([df, new_row_df], ignore_index=True)

        print("Income added successfully!")
        return results_df

    def save_csv(self, df):
        print("Save csv")

    def exit(self):
        print("Exit")