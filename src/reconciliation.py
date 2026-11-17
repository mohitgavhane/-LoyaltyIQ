
import pandas as pd
import os

DATA_FOLDER = "data"


def reconcile_points():

    print("\nLOYALTYIQ RECONCILIATION ENGINE")
    print("=" * 40)

    # Load datasets
    transactions = pd.read_csv(
        os.path.join(DATA_FOLDER, "transactions.csv")
    )

    earned = pd.read_csv(
        os.path.join(DATA_FOLDER, "points_earned.csv")
    )

    redeemed = pd.read_csv(
        os.path.join(DATA_FOLDER, "points_redeemed.csv")
    )

    expired = pd.read_csv(
        os.path.join(DATA_FOLDER, "points_expired.csv")
    )

    # Calculate expected points:
    # 1 point for every Rs. 100 spent
    transactions["expected_points"] = (
        transactions["purchase_amount"] // 100
    ).astype(int)

    # Compare expected and recorded earned points
    comparison = transactions.merge(
        earned,
        on=["transaction_id", "customer_id"],
        how="left"
    )

    comparison["points_earned"] = (
        comparison["points_earned"].fillna(0)
    )

    comparison["points_difference"] = (
        comparison["expected_points"]
        - comparison["points_earned"]
    )

    comparison["status"] = comparison[
        "points_difference"
    ].apply(
        lambda x: "Mismatch" if x != 0 else "Matched"
    )

    # Calculate customer-level totals
    earned_total = earned.groupby(
        "customer_id"
    )["points_earned"].sum()

    redeemed_total = redeemed[
        redeemed["status"].str.lower() == "completed"
    ].groupby("customer_id")[
        "points_redeemed"
    ].sum()

    expired_total = expired.groupby(
        "customer_id"
    )["points_expired"].sum()

    expected_total = comparison.groupby(
        "customer_id"
    )["expected_points"].sum()

    # Build customer balance report
    customers = pd.read_csv(
        os.path.join(DATA_FOLDER, "customers.csv")
    )

    report = customers[
        ["customer_id", "customer_name", "membership_tier"]
    ].copy()

    report["expected_points"] = (
        report["customer_id"].map(expected_total).fillna(0)
    )

    report["recorded_points"] = (
        report["customer_id"].map(earned_total).fillna(0)
    )

    report["redeemed_points"] = (
        report["customer_id"].map(redeemed_total).fillna(0)
    )

    report["expired_points"] = (
        report["customer_id"].map(expired_total).fillna(0)
    )

    report["expected_balance"] = (
        report["expected_points"]
        - report["redeemed_points"]
        - report["expired_points"]
    )

    report["recorded_balance"] = (
        report["recorded_points"]
        - report["redeemed_points"]
        - report["expired_points"]
    )

    report["balance_difference"] = (
        report["expected_balance"]
        - report["recorded_balance"]
    )

    report["reconciliation_status"] = (
        report["balance_difference"].apply(
            lambda x: "Mismatch" if x != 0 else "Matched"
        )
    )

    # Display transaction discrepancies
    mismatches = comparison[
        comparison["status"] == "Mismatch"
    ]

    print("\nTRANSACTION DISCREPANCIES")
    print("-" * 40)

    if mismatches.empty:
        print("No discrepancies found.")
    else:
        print(
            mismatches[
                [
                    "transaction_id",
                    "customer_id",
                    "expected_points",
                    "points_earned",
                    "points_difference",
                    "status"
                ]
            ].to_string(index=False)
        )

    # Display customer balances
    print("\nCUSTOMER BALANCE REPORT")
    print("-" * 40)

    print(report.to_string(index=False))

    # Summary measures
    print("\nSUMMARY")
    print("-" * 40)

    print("Total Customers:", len(report))
    print("Total Transactions:", len(transactions))
    print("Total Transaction Mismatches:", len(mismatches))
    print("Total Expected Points:", int(report["expected_points"].sum()))
    print("Total Redeemed Points:", int(report["redeemed_points"].sum()))
    print("Total Expired Points:", int(report["expired_points"].sum()))

    # Save reports
    os.makedirs("reports", exist_ok=True)

    comparison.to_csv(
        "reports/transaction_reconciliation.csv",
        index=False
    )

    report.to_csv(
        "reports/customer_balance_report.csv",
        index=False
    )

    print("\nReports saved successfully in the reports folder!")


if __name__ == "__main__":
    reconcile_points()
