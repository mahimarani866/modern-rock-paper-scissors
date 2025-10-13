import os
import pandas as pd


def main():
    # 1. Load historical data (2022-2024)
    df = pd.read_csv("data/monthly_financials.csv", parse_dates=["Month"])
    df = df.sort_values("Month")

    # Basic profit calculation
    df["Profit"] = df["Revenue"] - df["Expenses"]

    # 2. Simple time-series forecasting (moving average)
    # Use 3-month moving average as a very simple forecast method
    df["Revenue_MA3"] = df["Revenue"].rolling(window=3).mean()
    df["Expenses_MA3"] = df["Expenses"].rolling(window=3).mean()

    # Last known moving averages
    last_rev_ma3 = df["Revenue_MA3"].iloc[-1]
    last_exp_ma3 = df["Expenses_MA3"].iloc[-1]

    # 3. Create forecast for next 12 months (2025)
    last_month = df["Month"].max()
    forecast_months = pd.date_range(last_month, periods=12, freq="M") + pd.offsets.MonthEnd(0)

    forecast_df = pd.DataFrame(
        {
            "Month": forecast_months,
            "Revenue_Forecast": [last_rev_ma3] * 12,
            "Expenses_Forecast": [last_exp_ma3] * 12,
        }
    )
    forecast_df["Profit_Forecast"] = forecast_df["Revenue_Forecast"] - forecast_df["Expenses_Forecast"]

    # 4. Simple scenario analysis (what-if)
    # Use the last actual month (Dec-2024) as base
    last_row = df.iloc[-1]
    base_revenue = last_row["Revenue"]
    base_expenses = last_row["Expenses"]
    base_profit = last_row["Profit"]

    scenarios = [
        {
            "Scenario": "Best Case",
            "Revenue": base_revenue * 1.10,   # +10% revenue
            "Expenses": base_expenses * 0.95  # -5% expenses
        },
        {
            "Scenario": "Expected",
            "Revenue": base_revenue * 1.02,   # +2% revenue
            "Expenses": base_expenses * 1.00  # same expenses
        },
        {
            "Scenario": "Worst Case",
            "Revenue": base_revenue * 0.90,   # -10% revenue
            "Expenses": base_expenses * 1.05  # +5% expenses
        },
    ]

    scenario_rows = []
    for s in scenarios:
        profit = s["Revenue"] - s["Expenses"]
        scenario_rows.append(
            {
                "Scenario": s["Scenario"],
                "Revenue": round(s["Revenue"], 2),
                "Expenses": round(s["Expenses"], 2),
                "Profit": round(profit, 2),
                "Delta_vs_Current_Profit": round(profit - base_profit, 2),
            }
        )

    scenario_df = pd.DataFrame(scenario_rows)

    # 5. Save everything to Excel files
    os.makedirs("outputs", exist_ok=True)

    hist_path = "outputs/historical_financials.xlsx"
    forecast_path = "outputs/forecast_2025.xlsx"
    scenario_path = "outputs/scenario_analysis.xlsx"

    df.to_excel(hist_path, index=False)
    forecast_df.to_excel(forecast_path, index=False)
    scenario_df.to_excel(scenario_path, index=False)

    print("✅ Historical data saved to:", hist_path)
    print("✅ Forecast for 2025 saved to:", forecast_path)
    print("✅ Scenario analysis saved to:", scenario_path)

    # 6. Small summary for you (console only)
    print("\n=== Quick Summary ===")
    print("Last actual month:", last_month.date())
    print("Base profit (Dec-2024):", base_profit)
    print("\nScenario analysis:")
    print(scenario_df)


if __name__ == "__main__":
    main()
