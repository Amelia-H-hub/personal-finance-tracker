# This file will define functions about data analysis
import matplotlib.pyplot as plt
import pandas as pd

class Analysis:
    def analyze_spending_category(self, df):
        if df.empty:
            return df
        
        print()
        print("--- Total Spending by Category ---")

        total_spending_by_category = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum().sort_index()
        print(total_spending_by_category.to_string())

    def calculate_average_monthly_spending(self, df):
        if df.empty:
            return df
        
        print()
        print("--- Average Monthly Spending ---")

        avg = round(df[df["Type"] == "Expense"].groupby(df["Date"].dt.to_period('M'))["Amount"].mean().mean(), 2)
        print(avg)

    def show_top_spending_category(self, df):
        print()
        if df.empty:
            print("No data to analyze.")
            return

        spending_df = df[df["Type"] == "Expense"]
        top_category = spending_df.groupby("Category")["Amount"].sum().idxmax()
        max_amount = spending_df.groupby("Category")["Amount"].sum().max()

        print(f"Top spending category: {top_category} (${max_amount:.2f})")

    def visualize_spending_trends(self, df):
        print("Visualize Spending Trends")
        if df.empty:
            print("No data to visualize.")
            return

            # Ensure date column is datetime and keep only expenses
        df = df.copy()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df[df["Type"].str.lower() == "expense"]

        if df.empty:
            print("No expense rows to visualize.")
            return

        # Aggregate by month
        df["YearMonth"] = df["Date"].dt.to_period("M")
        monthly = df.groupby("YearMonth")["Amount"].sum()
        x = monthly.index.to_timestamp()  # convert PeriodIndex → Timestamp
        y = monthly.values

        # ----- Line chart -----
        plt.figure(figsize=(8, 4))
        plt.plot(x, y, marker="o", linewidth=2)
        plt.title("Monthly Spending Trend")
        plt.xlabel("Month")
        plt.ylabel("Total Spending")
        plt.grid(alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()