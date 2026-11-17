
# LoyaltyIQ
## Customer Loyalty and Reward Reconciliation

### 1. Project Overview
LoyaltyIQ is a Customer Loyalty and Reward Reconciliation system developed to manage customer transactions, calculate loyalty points, track redemptions and expirations, and identify discrepancies in loyalty point records.

The project uses Python, Pandas, NumPy, SQLite, Streamlit, and Plotly.

### 2. Problem Statement
Customer Loyalty and Reward Reconciliation

### 3. Objectives
- Clean and process customer and transaction datasets.
- Calculate expected loyalty points.
- Compare expected and recorded points.
- Identify mismatches in loyalty transactions.
- Calculate customer point balances.
- Store processed data in an SQLite database.
- Display insights using an interactive dashboard.

### 4. Technologies Used
- Python
- Pandas
- NumPy
- SQLite
- Streamlit
- Plotly
- VS Code

### 5. Project Structure
```text
LoyaltyIQ/
│
├── data/
│   ├── customers.csv
│   ├── transactions.csv
│   ├── points_earned.csv
│   ├── points_redeemed.csv
│   └── points_expired.csv
│
├── database/
│   └── loyaltyiq.db
│
├── reports/
│   ├── transaction_reconciliation.csv
│   └── customer_balance_report.csv
│
├── src/
│   ├── data_cleaning.py
│   ├── reconciliation.py
│   └── database.py
│
├── app.py
├── requirements.txt
└── README.md
```

### 6. Working Methodology
1. Load customer, transaction, earned, redeemed, and expired points datasets.
2. Clean the datasets by removing duplicate and missing records.
3. Calculate expected points using the rule of 1 point for every ₹100 spent.
4. Compare expected points with recorded points.
5. Calculate customer balances after redemptions and expirations.
6. Store processed datasets and reports in SQLite.
7. Display results through the Streamlit dashboard.

### 7. Dashboard Features
- Business Overview
- Customer Analysis
- Points Reconciliation
- Transaction Records
- Customer balance analysis
- Interactive charts and reports

### 8. Expected Outcomes
- Identification of loyalty point mismatches.
- Accurate calculation of expected customer balances.
- Better visibility into customer loyalty activity.
- Easier inspection of transaction records.
- Improved reward reconciliation and reporting.

### 9. How to Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run data cleaning:

```bash
python src/data_cleaning.py
```

Run reconciliation:

```bash
python src/reconciliation.py
```

Create and populate the database:

```bash
python src/database.py
```

Launch the dashboard:

```bash
streamlit run app.py
```

### 10. Conclusion
LoyaltyIQ demonstrates an end-to-end data engineering and visualization workflow. It processes multiple datasets, performs data cleaning and reconciliation, stores processed information in SQLite, and presents useful customer loyalty insights through an interactive dashboard.
