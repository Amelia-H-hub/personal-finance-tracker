# This file will define functions about data analysis

class Analysis:
    def analyze_spending_category(self, df):
        if df.empty:
            return df
        
        print("Analyze Spending Category")
        print("--- Total Spending by Category ---")

        total_spending_by_category = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum().sort_index()
        print(total_spending_by_category.to_string())

    def calculate_average_monthly_spending(self, df):
        if df.empty:
            return df
        
        print("Calculate Average Monthly Spending")
        print("--- Average Monthly Spending ---")

        avg = round(df[df["Type"] == "Expense"].groupby(df["Date"].dt.to_period('M'))["Amount"].mean().mean(), 2)
        print(avg)

    def show_top_spending_category(self, df):
        print("Show Top Spending Category")

    def visualize_spending_trends(self, df):
        print("Visualize Spending Trends")