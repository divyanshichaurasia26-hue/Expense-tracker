import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("💸 Personal Expense Tracker")
st.write("App loading...")

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Expense Tracker", layout="wide")

# ---------- CUSTOM UI ----------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
h1 {
    color: #2c3e50;
}
div[data-testid="metric-container"] {
    background-color: #ffffff;
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("💸 Personal Expense Tracker")
st.markdown("Track, analyze and improve your spending habits 💡")

# ---------- LOAD DATA ----------
def load_data():
    df = pd.read_csv("expenses.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("🔍 Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

start_date = st.sidebar.date_input("Start Date", value=min_date)
end_date = st.sidebar.date_input("End Date", value=max_date)

categories = st.sidebar.multiselect(
    "Select Categories",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# ---------- APPLY FILTER ----------
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_df = df[
    (df["Date"] >= start_date) &
    (df["Date"] <= end_date) &
    (df["Category"].isin(categories))
]

filtered_df = filtered_df.sort_values(by="Date", ascending=False)

# ---------- ADD EXPENSE ----------
st.subheader("➕ Add New Expense")

col1, col2, col3, col4 = st.columns(4)

with col1:
    date = st.date_input("Date")

with col2:
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Health", "Entertainment"])

with col3:
    amount = st.number_input("Amount", min_value=0)

with col4:
    description = st.text_input("Description")

if st.button("Add Expense"):
    new_data = pd.DataFrame([[date, category, amount, description]],
                            columns=["Date", "Category", "Amount", "Description"])
    
    new_data.to_csv("expenses.csv", mode='a', header=False, index=False)
    st.success("Expense Added!")
    st.rerun()

# ---------- METRICS ----------
st.subheader("📊 Dashboard Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Total Spending", f"₹ {filtered_df['Amount'].sum()}")

with col2:
    st.metric("📊 Transactions", len(filtered_df))

with col3:
    st.metric("📂 Categories", filtered_df["Category"].nunique())

# ---------- CHARTS ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Category Spending")
    category_data = filtered_df.groupby("Category")["Amount"].sum()
    st.bar_chart(category_data)

with col2:
    st.subheader("📆 Monthly Trend")
    filtered_df["Month"] = filtered_df["Date"].dt.to_period("M")
    monthly = filtered_df.groupby("Month")["Amount"].sum()
    st.line_chart(monthly)

# ---------- PIE CHART ----------
st.subheader("📈 Spending Distribution")

fig, ax = plt.subplots()
category_data.plot(kind='pie', autopct='%1.1f%%', ax=ax)
st.pyplot(fig)

# ---------- DATA TABLE ----------
st.subheader("📋 Detailed Data")
st.dataframe(filtered_df, use_container_width=True)

# ---------- DOWNLOAD BUTTON ----------
st.subheader("📥 Download Report")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name='expense_report.csv',
    mime='text/csv',
)
