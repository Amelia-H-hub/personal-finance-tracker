# This file will define functions for operating transactions

from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pandas as pd

class Transaction:
    def __init__(self):
        self.file_path = None
        self.is_trans_saved = False

    def import_csv(self):
        # hide the main window
        Tk().withdraw()

        # choose a file
        self.file_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not self.file_path:
            print("Cancelled.", "No data imported.")
            return

        # read the csv file
        df = pd.read_csv(self.file_path)
        df["Date"] = pd.to_datetime(df["Date"])
        df.index = range(1, len(df) + 1)
        self.is_trans_saved = False
        print("\nLoad transaction data successfully!")
        return df

    def view_transaction(self, df):
        print(df)
        while True:
            quit = input("Press Q to quit: ").strip().lower()
            if quit == 'q':
                return

    def view_transactions_filter(self, df):
        # remain all data at first
        filters = pd.Series([True] * len(df), index=df.index)

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

        filtered_transactions = df[filters]
        print(f"\n{filtered_transactions}\n")
        while True:
            quit = input("Press Q to quit: ").strip().lower()
            if quit == 'q':
                return

    def add_transaction(self, df):
        print("Add transactions")
        date = input("Enter the date: yyyy-mm-dd ")
        category = input("Enter the category:  ")
        description = input("Enter the description: ")


        while True:
            try:
                amount = float(input("Enter the amount: "))
                break
            except ValueError:
                print("Please enter a number.")

        new_transaction = {
            "Date": pd.to_datetime(date),
            "Category": category,
            "Description": description,
            "Amount": amount,
            "Type" : "Expense",
        }



        new_row_df = pd.DataFrame([new_transaction])

        if df.empty:
            df = new_row_df
        else:
             df = pd.concat([df, new_row_df], ignore_index=True)

        df.index = range(1,len(df)+1)
        self.is_trans_saved = False
        print("Transaction added successfully")
        return df

    def edit_transaction(self, df):
        print("Edit transactions")
        if df.empty:
            return df
        
        # Get the index of the transaction
        while True:
            try:
                index = int(input("Enter the index of the transaction to edit: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            except Exception:
                print("An unexpected error occurred.")
                continue

            if index < 1 or index > len(df):
                print("Invalid index. Please enter again.")
                continue

            print()
            break

        # Subtract 1 because the DataFrame index starts at 1
        index -= 1
        
        # Display current transaction details
        print("Current Transaction Details:")
        print(f"Date: {df.loc[df.index[index], "Date"].date()}")
        print(f"Category: {df.loc[df.index[index], "Category"]}")
        print(f"Description: {df.loc[df.index[index], "Description"]}")
        print(f"Amount: {df.loc[df.index[index], "Amount"]}")
        print()

        # Get the date
        while True:
            try:
                s = input("Enter new date (YYYY-MM-DD) or press Enter to keep current: ")
                if not s:
                    date = df.loc[df.index[index], "Date"]
                else:
                    date = pd.to_datetime(s)
                break
            except ValueError:
                print("Invalid input. Please enter a valid date.")
                continue
            except Exception:
                print("An unexpected error occurred.")
                continue

        # Get the category
        while True:
            try:
                category = input("Enter new category or press Enter to keep current: ")
                if not category:
                    category = df.loc[df.index[index], "Category"]
                break
            except Exception:
                print("An unexpected error occurred.")
                continue
        
        # Get a description
        while True:
            try:
                desc = input("Enter new description or press Enter to keep current: ")
                if not desc:
                    desc = df.loc[df.index[index], "Description"]
                break
            except Exception:
                print("An unexpected error occurred.")
                continue
        
        # Get the amount
        while True:
            try:
                s = input("Enter new amount or press Enter to keep current: ")
                if not s:
                    amount = df.loc[df.index[index], "Amount"]
                else:
                    amount = round(pd.to_numeric(s), 2)       
                    if amount <= 0:
                        print("Invalid input. Please enter a value greater than 0.01.")
                        continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            except Exception:
                print("An unexpected error occurred.")
                continue

        # Create a new row
        new_row = {
            "Date" : date,
            "Category" : category,
            "Description" : desc,
            "Amount" : amount,
            "Type" : df.loc[df.index[index], "Type"]
        }

        # Update table with new row
        df.iloc[index] = new_row

        print()
        print("Transaction updated successfully!")
        self.is_trans_saved = False
        return df


    def delete_transaction(self, df):
        print("Delete transactions")
        while True:
            try:
                delete_index = int(input("Enter the index of the transaction to delete: "))

                if delete_index in df.index:
                    df = df.drop(delete_index)
                    print("Transaction deleted successfully!")
                    break
                else:
                    print(f"Error: Index {delete_index} not found. Please try again.")

            except ValueError:
                print("Invalid input. Please enter a valid integer index.")

        self.is_trans_saved = False
        return df

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
        self.is_trans_saved = False
        results_df.index = range(1,len(results_df)+1)

        print("Income added successfully!")
        return results_df

    def save_csv(self, df):
        root = Tk()
        root.withdraw()

        if not self.file_path:
            self.file_path = asksaveasfilename(defaultextension=".csv",
                                          filetypes=[("CSV files", "*.csv")],
                                          title="Save as")
            if not self.file_path:
                print("Cancelled", "Transaction didn't save.")
                return

        else:
            confirm = input(
                f"Do you want to overwrite transactions in {self.file_path}? (Y/n): ").strip().lower()
            if confirm not in ["y", "n", ""]:
                print("Invalid input. Please enter either 'y' or 'n' or just press enter for 'y'.")
            elif confirm == 'n':
                print("Transactions didn't save.")
                return

        try:
            df.to_csv(self.file_path, index=False)
            self.is_trans_saved = True
            print(f"File saved to {self.file_path}")
        except Exception as e:
            print(f"Error. Failed to save: {e}")

    def exit(self, is_budget_saved):
        if not self.is_trans_saved:
            is_quit = input("Transactions haven't been saved. Are you sure to quit? (Y/n) ").strip().lower()
            if is_quit in ["y", "n", ""]:
                if is_quit == "n":
                    return
            else:
                print("Invalid input. Please enter either 'y' or 'n' or just press enter for 'y'.")

        if not is_budget_saved:
            is_quit_without_budget = input(
                "Budget haven't been saved. Are you sure to quit? (Y/n) ").strip().lower()
            if is_quit_without_budget in ["y", "n", ""]:
                if is_quit_without_budget == "n":
                    return
            else:
                print("Invalid input. Please enter either 'y' or 'n' or just press enter for 'y'.")
        print("Goodbye! Your session has ended.")
        exit()
