import pandas as pd
import matplotlib.pyplot as plt

from budget import Budget
from transaction import Transaction
from budget import Budget
from analysis import Analysis

def main():
    ts = Transaction()
    bg = Budget()
    an = Analysis()

    columns = ["Date", "Category", "Description", "Amount", "Type"]
    df = pd.DataFrame(columns=columns)
    columns_budget = ["Date", "Category", "Amount"]
    budget = pd.DataFrame(columns=columns_budget)

    print("===Hi! I'm your personal finance tracker===")

    while True:
        print("Choose an action below:")
        print("1. Import a CSV File")
        print("2. View all transactions")
        print("3. View transactions by date range, category, type")
        print("4. Add a transaction")
        print("5. Edit an existing transaction")
        print("6. Delete a transaction")
        print("7. Analyze Spending by Category")
        print("8. Calculate Average Monthly Spending")
        print("9. Show Top Spending Category")
        print("10. Set Monthly Income")
        print("11. Set Category Budget")
        print("12. Check Budget Status")
        print("13. Visualize Spending Trends")
        print("14. Save Transactions to CSV")
        print("15. Quit")

        try:
            operation = int(input("Choose an action below: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 15.")
            continue
        except Exception:
            print("An unexpected error occurred.")
            continue

        if operation == 1:
            df = ts.import_csv()
        elif operation == 2:
            ts.view_transaction(df)
        elif operation == 3:
            ts.view_transactions_filter(df)
        elif operation == 4:
            df = ts.add_transaction()
        elif operation == 5:
            df = ts.edit_transaction(df)
        elif operation == 6:
            df = ts.delete_transaction(df)
        elif operation == 7:
            an.analyze_spending_category(df)
        elif operation == 8:
            an.calculate_average_monthly_spending(df)
        elif operation == 9:
            an.show_top_spending_category(df)
        elif operation == 10:
            df = ts.set_income(df)
        elif operation == 11:
            budget = bg.set_budget(budget)
        elif operation == 12:
            bg.check_budget(budget)
        elif operation == 13:
            an.visualize_spending_trends(df)
        elif operation == 14:
            ts.save_csv(df)
        elif operation == 15:
            ts.exit()

if __name__ == "__main__":
    main()
