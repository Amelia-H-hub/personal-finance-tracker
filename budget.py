# This file will define functions about the budget
from operator import index
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pandas as pd

class Budget:
    def __init__(self):
        self.budget_path = None
        self.is_budget_saved = False

    def import_budget(self):
        Tk().withdraw()

        # choose a file
        self.budget_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not self.budget_path:
            print("Cancelled.", "No data imported.")
            return

        # read the csv file
        budget = pd.read_csv(self.budget_path)
        try:
            budget["Month"] = pd.to_datetime(budget["Month"], format="%Y-%m").dt.to_period("M")
        except ValueError:
            print("Invalid month format. Please check your data in the file")
        print("Load budget successfully!", self.budget_path)
        self.is_budget_saved = False
        return budget, self.is_budget_saved

    def set_budget(self, budget, df):
        categories = df["Category"].unique().tolist()
        while True:
            month = input("Enter the year and month of your budget (YYYY-MM): ").strip()
            try:
                month = pd.to_datetime(month, format="%Y-%m").to_period("M")
            except ValueError:
                print("Invalid format. Please enter a valid month in YYYY-MM format.")
                continue
            break

        while True:
            print("Choose a category below:")
            for i in range(len(categories)):
                print(categories[i])
            category = input("Enter the category of your budget: ").strip()
            if not category:
                print("Please enter a valid category.")
                continue
            if category not in categories:
                isNewCategory = input(f"Category not found in your transaction list. Are you sure you want to create a budget of {category}? (Y/n) ").strip().lower()
                if isNewCategory.lower() == "n":
                    continue
            break

        while True:
            budgetAmount = input("Enter the amount of your budget: ").strip()
            try:
                budgetAmount = float(budgetAmount)
                if budgetAmount < 0:
                    print("Invalid budget. Negative values are not allowed.")
                    continue
            except ValueError:
                print("Invalid budget. Please enter a valid number.")
                continue
            break

        existing = budget[(budget["Month"] == month) & (budget["Category"] == category)]

        if not existing.empty:
            print("A budget for this month and category already exists.")
            isOverwrite = input("Do you want to update this budget? (Y/n) ").strip().lower()
            if isOverwrite == "y" or isOverwrite == "":
                budget[(budget["Month"] == month) & (budget["Category"] == category), "Budget"] = budgetAmount
                print(f"Budget for {month} of {category} has been updated.")
            else:
                print("No changes made.")
                return
        else:
            new_budget = {
                "Month": month,
                "Category": category,
                "Budget": budgetAmount
            }
            budget.loc[len(budget)] = new_budget

        self.is_budget_saved = False
        print(budget, index=False)
        return budget, self.is_budget_saved

    def check_budget(self, budget, df):
        if budget.empty:
            print("No budget data!")
            return
        if df.empty:
            print("No transaction data!")
            return
        while True:
            month = input("Enter the year and month to check your budget (YYYY-MM) or press Q to quit: ").strip()
            if month.lower() == "q":
                return
            try:
                month = pd.to_datetime(month, format="%Y-%m").to_period("M")
            except ValueError:
                print("Invalid format. Please enter a valid month in YYYY-MM format.")
                continue

            budget_target_month = budget[budget["Month"] == month]
            if budget_target_month.empty:
                print("No budget for this month.")
                continue
            df["Month"] = df["Date"].dt.to_period("M")
            transactions_target_month = df[df["Month"] == month]
            if transactions_target_month.empty:
                print("No transactions for this month.")
                continue
            transactions_category_sum = transactions_target_month.groupby("Category")["Amount"].sum().reset_index()
            merged_df = pd.merge(budget_target_month, transactions_category_sum, on="Category", how="outer")
            merged_df["Month"] = month
            merged_df = merged_df[merged_df["Category"] != "Income"]
            merged_df = merged_df.rename(columns={"Amount": "Expense"})
            merged_df = merged_df[["Month", "Category", "Expense", "Budget"]]
            print(merged_df.to_string(index=False))
            break

        over_budget = merged_df[(merged_df["Budget"].notna()) & (merged_df["Expense"] > merged_df["Budget"])]
        near_budget = merged_df[(merged_df["Budget"].notna()) & ((merged_df["Budget"] - merged_df["Expense"]) > 0) & ((merged_df["Budget"] - merged_df["Expense"]) < 50)]

        if not over_budget.empty or not near_budget.empty:
            print("\n=====Heads up!=====")
        else:
            print("✅ You stayed within your budget for all categories!")

        if not over_budget.empty:
            print("⚠️ You have exceeded your budget in the following categories:")
            for _, rowOver in over_budget.iterrows():
                print(f"{rowOver['Category']}: ${rowOver['Expense']:.2f} / ${rowOver['Budget']:.2f}; Over Budget Amount: ${rowOver['Expense'] - rowOver['Budget']:.2f}")
            print()

        if not near_budget.empty:
            print("⚠️ You are close to exceeding your budget in the following categories:")
            for _, rowClose in near_budget.iterrows():
                print(f"{rowClose['Category']}: ${rowClose['Expense']:.2f} / ${rowClose['Budget']:.2f}; Left Budget Amount: ${rowClose['Budget'] - rowClose['Expense']:.2f}")
            print()

        while True:
            quit = input("Press Q to quit: ").strip().lower()
            if quit == 'q':
                return

    def save_budget_csv(self, budget):
        root = Tk()
        root.withdraw()

        if not self.budget_path:
            self.budget_path = asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("CSV files", "*.csv")],
                                               title="Save as")
            if not self.budget_path:
                print("Cancelled", "Budget didn't save.")
                return

        else:
            confirm = input(
                f"Do you want to overwrite the budget in {self.budget_path}? (Y/n): ").strip().lower()
            if confirm not in ["y", "n", ""]:
                print("Invalid input. Please enter either 'y' or 'n' or just press enter for 'y'.")
            elif confirm == 'n':
                print("Budget didn't save.")
                return

        budget.to_csv(self.budget_path, index=False)
        self.is_budget_saved = True
        print(f"Budget saved to {self.budget_path}")

        return self.is_budget_saved
