
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="LoyaltyIQ",
    page_icon="🎯",
    layout="wide"
)

DB_PATH = "database/loyaltyiq.db"

# ---------------- DATABASE CONNECTION ----------------

@st.cache_data
def load_data():

    if not os.path.exists(DB_PATH):
        return None, None

    conn = sqlite3.connect(DB_PATH)

    try:
        customers = pd.read_sql(
            "SELECT * FROM customers", conn
        )

        balances = pd.read_sql(
            "SELECT * FROM customer_balance_report", conn
        )

        transactions = pd.read_sql(
            "SELECT * FROM transaction_reconciliation", conn
        )

        conn.close()

        return customers, balances, transactions

    except Exception as e:
        conn.close()
        st.error(f"Database error: {e}")
        return None, None, None


# ---------------- SIDEBAR ----------------

st.sidebar.title("🎯 LoyaltyIQ")

st.sidebar.markdown(
    "Customer Loyalty & Reward Reconciliation"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Customer Analysis",
        "Points Reconciliation",
        "Transaction Records",
        "About Project"
    ]
)

# ---------------- LOAD DATA ----------------

result = load_data()

if result[0] is None:
    st.error(
        "Database not found. Please run the reconciliation "
        "and database scripts first."
    )
    st.stop()

customers, balances, transactions = result

# ---------------- DASHBOARD ----------------

st.title("🎯 LoyaltyIQ")
st.subheader("Customer Loyalty Analytics Platform")

st.caption(
    "Data Engineering and Visualization Lab | 23CSE3159"
)

if page == "Dashboard":

    st.markdown("### Business Overview")

    total_customers = len(customers)

    total_transactions = len(transactions)

    total_points = int(
        balances["expected_points"].sum()
    )

    total_redeemed = int(
        balances["redeemed_points"].sum()
    )

    total_expired = int(
        balances["expired_points"].sum()
    )

    mismatch_count = int(
        (transactions["status"] == "Mismatch").sum()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Customers", total_customers)

    col2.metric("Total Transactions", total_transactions)

    col3.metric("Expected Points", f"{total_points:,}")

    col4, col5, col6 = st.columns(3)

    col4.metric("Points Redeemed", f"{total_redeemed:,}")

    col5.metric("Points Expired", f"{total_expired:,}")

    col6.metric("Transaction Mismatches", mismatch_count)

    st.divider()

    st.markdown("### Customer Membership Distribution")

    tier_data = customers["membership_tier"].value_counts()

    fig = px.pie(
        names=tier_data.index,
        values=tier_data.values,
        title="Customers by Membership Tier",
        hole=0.45
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Customer Points Overview")

    fig2 = px.bar(
        balances,
        x="customer_name",
        y=[
            "expected_points",
            "redeemed_points",
            "expired_points"
        ],
        barmode="group",
        title="Customer Loyalty Points Analysis"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Customer Balance Records")

    st.dataframe(
        balances,
        use_container_width=True,
        hide_index=True
    )


# ---------------- CUSTOMER ANALYSIS ----------------

elif page == "Customer Analysis":

    st.header("👥 Customer Analysis")

    customer_names = balances["customer_name"].tolist()

    selected = st.selectbox(
        "Select Customer",
        customer_names
    )

    customer = balances[
        balances["customer_name"] == selected
    ]

    st.dataframe(
        customer,
        use_container_width=True,
        hide_index=True
    )

    row = customer.iloc[0]

    c1, c2, c3 = st.columns(3)

    c1.metric("Expected Balance", int(row["expected_balance"]))

    c2.metric("Recorded Balance", int(row["recorded_balance"]))

    c3.metric("Difference", int(row["balance_difference"]))

    customer_id = row["customer_id"]

    customer_transactions = transactions[
        transactions["customer_id"] == customer_id
    ]

    st.subheader("Customer Transaction History")

    st.dataframe(
        customer_transactions,
        use_container_width=True,
        hide_index=True
    )


# ---------------- RECONCILIATION ----------------

elif page == "Points Reconciliation":

    st.header("🔍 Points Reconciliation")

    st.write(
        "Compare expected loyalty points with recorded points."
    )

    mismatches = transactions[
        transactions["status"] == "Mismatch"
    ]

    matched = transactions[
        transactions["status"] == "Matched"
    ]

    c1, c2 = st.columns(2)

    c1.metric("Matched Transactions", len(matched))

    c2.metric("Mismatched Transactions", len(mismatches))

    st.subheader("Discrepancy Records")

    if len(mismatches) > 0:

        st.dataframe(
            mismatches,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success("No discrepancies found!")

    st.subheader("Reconciliation Status")

    fig = px.pie(
        names=["Matched", "Mismatch"],
        values=[len(matched), len(mismatches)],
        title="Transaction Reconciliation Results"
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------- TRANSACTION RECORDS ----------------

elif page == "Transaction Records":

    st.header("📋 Transaction Records")

    search = st.text_input(
        "Search by Customer ID or Transaction ID"
    )

    filtered = transactions.copy()

    if search:

        filtered = filtered[
            filtered["customer_id"].astype(str).str.contains(
                search, case=False
            )
            |
            filtered["transaction_id"].astype(str).str.contains(
                search, case=False
            )
        ]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Transaction Report",
        filtered.to_csv(index=False),
        file_name="loyaltyiq_transaction_report.csv",
        mime="text/csv"
    )


# ---------------- ABOUT PROJECT ----------------

elif page == "About Project":

    st.header("About LoyaltyIQ")

    st.write("""
    LoyaltyIQ is a Customer Loyalty and Reward Reconciliation
    System developed for the Data Engineering and Visualization Lab.

    The application processes customer profiles, purchases,
    earned points, redeemed points and expired points.

    It identifies differences between expected and recorded
    loyalty points and generates customer balance reports.
    """)

    st.subheader("Technology Stack")

    st.write("""
    - Python
    - Pandas
    - NumPy
    - SQLite
    - Streamlit
    - Plotly
    """)

    st.subheader("Data Engineering Pipeline")

    st.write("""
    Extract → Transform → Load → Reconcile → Analyze → Visualize
    """)


st.sidebar.divider()

st.sidebar.caption("LoyaltyIQ | Academic Mini Project")
