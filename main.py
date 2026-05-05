import pandas as pd

def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))
    desc = input("Enter description: ")

    new_data = pd.DataFrame([[date, category, amount, desc]],
                            columns=["Date", "Category", "Amount", "Description"])

    new_data.to_csv("expenses.csv", mode='a', header=False, index=False)

    print("Expense added successfully!")

add_expense()

def total_spending():
    df = pd.read_csv("expenses.csv")
    print("Total Spending:", df["Amount"].sum())

total_spending()

def category_spending():
    df = pd.read_csv("expenses.csv")
    print(df.groupby("Category")["Amount"].sum())

category_spending()

import matplotlib.pyplot as plt

def plot_expenses():
    df = pd.read_csv("expenses.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    data = df.groupby("Category")["Amount"].sum()

    data.plot(kind='bar')
    plt.title("Category-wise Spending")
    plt.ylabel("Amount")
    plt.show()

plot_expenses()

def monthly_spending():
    df = pd.read_csv("expenses.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    
    df["Month"] = df["Date"].dt.month
    print(df.groupby("Month")["Amount"].sum())