# This file will define functions for operating transactions

from datetime import datetime
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pandas as pd

class Transaction:
    def import_csv(self):
        # hide the main window
        Tk().withdraw()

        # choose a file
        self.file_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
        print("Load file successfully:", self.file_path)

        # read the csv file
        df = pd.read_csv(self.file_path)
        df["Date"] = pd.to_datetime(df["Date"])
        return df

    def view_transaction(self, df):
        print(df)

    def view_transactions_filter(self, df):
        # remain all data at first
        filters = pd.Series([True] * len(df))

        while True:
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            if start_date:
                try:
                    datetime.strptime(start_date, "%Y-%m-%d")
                    start_date = pd.to_datetime(start_date)
                    filters &= df["Date"] >= start_date
                except ValueError:
                    print("Invalid date. Please enter a valid date in YYYY-MM-DD format.")
                    continue
            break

        while True:
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()
            if end_date:
                try:
                    datetime.strptime(end_date, "%Y-%m-%d")
                    end_date = pd.to_datetime(end_date)
                    filters &= df["Date"] <= end_date
                except ValueError:
                    print("Invalid date. Please enter a valid date in YYYY-MM-DD format.")
                    continue
            break

        while True:
            print("Choose a category below:")
            categories = df["Category"].unique().tolist()
            for i in range(len(categories)):
                print(categories[i])
            category = input(
                "Enter transaction category. If nothing is entered, the result will include all categories: ").strip()
            if category not in categories and category != "":
                print("Category not found. Please choose an exist category.")
                continue
            elif category:
                filters &= df["Category"] == category
            break

        while True:
            type = input(
                "Enter a type either 'Expense' or 'Income'. If nothing is entered, the result will include all types: ")
            if type != "" and type not in ["Expense", "Income"]:
                print("Invalid type. Please enter either 'Expense' or 'Income'.")
                continue
            elif type:
                filters &= df["Type"] == type
            break

        filtered_transactions = df[filters]
        print(f"{filtered_transactions}\n")

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
        root = Tk()
        root.withdraw()

        if not self.file_path:
            self.file_path = asksaveasfilename(defaultextension=".csv",
                                          filetypes=[("CSV files", "*.csv")],
                                          title="Save as")
            if not self.file_path:
                print("Canceled", "Transaction didn't save.")
                return

        else:
            confirm = messagebox.askyesno("Confirm Overwrite",
                                          f"Do you want to overwrite transactions in {self.file_path}?")
            if not confirm:
                messagebox.showinfo("Canceled", "Transactions didn't save.")
                return

        df.to_csv(self.file_path, index=False)
        print(f"File saved to {self.file_path}")

    def exit(self):
        print("Exit")