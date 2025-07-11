import pandas as pd

from transaction import Transaction
from budget import Budget
from analysis import Analysis


def main():
    ts = Transaction()
    bg = Budget()
    an = Analysis()

    columns = ["Date", "Category", "Description", "Amount", "Type"]
    df = pd.DataFrame(columns=columns)
    columns_budget = ["Month", "Category", "Budget"]
    budget = pd.DataFrame(columns=columns_budget)
    is_budget_saved = True

    print("\n===Hi! I'm your personal finance tracker===")

    while True:
        print("\nChoose an action below:")
        print("1. Import a CSV file of transactions")
        print("2. Import a CSV file of budget")
        print("3. View all transactions")
        print("4. View transactions by date range, category")
        print("5. Add an expense")
        print("6. Add an Income")
        print("7. Edit an existing transaction")
        print("8. Delete a transaction")
        print("9. Analyze Spending by Category")
        print("10. Calculate Average Monthly Spending")
        print("11. Show Top Spending Category")
        print("12. Set Category Budget")
        print("13. Check Budget Status")
        print("14. Visualize Spending Trends")
        print("15. Save Transactions to CSV")
        print("16. Save Budget to CSV")
        print("17. Quit")

        try:
            operation = int(input("\nEnter the number of the action: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 15.")
            continue
        except Exception:
            print("An unexpected error occurred.")
            continue

        if operation == 1:
            df = ts.import_csv()
        elif operation == 2:
            budget, is_budget_saved = bg.import_budget()
        elif operation == 3:
            ts.view_transaction(df)
        elif operation == 4:
            ts.view_transactions_filter(df)
        elif operation == 5:
            df = ts.add_transaction(df)
        elif operation == 6:
            df = ts.set_income(df)
        elif operation == 7:
            df = ts.edit_transaction(df)
        elif operation == 8:
            df = ts.delete_transaction(df)
        elif operation == 9:
            an.analyze_spending_category(df)
        elif operation == 10:
            an.calculate_average_monthly_spending(df)
        elif operation == 11:
            an.show_top_spending_category(df)
        elif operation == 12:
            budget, is_budget_saved = bg.set_budget(budget, df)
        elif operation == 13:
            bg.check_budget(budget, df)
        elif operation == 14:
            an.visualize_spending_trends(df)
        elif operation == 15:
            ts.save_csv(df)
        elif operation == 16:
            is_budget_saved = bg.save_budget_csv(budget)
        elif operation == 17:
            ts.exit(is_budget_saved)

if __name__ == "__main__":
    main()
