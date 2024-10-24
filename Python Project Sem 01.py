import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import csv

class ExpenseManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Manager")
        self.root.geometry("500x400")

        # Create input frame
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.pack(fill=tk.X)

        # Date input
        self.date_label = tk.Label(input_frame, text="Date (YYYY-MM-DD)")
        self.date_label.grid(row=0, column=0, sticky=tk.W)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1)

        # Description input
        self.description_label = tk.Label(input_frame, text="Description")
        self.description_label.grid(row=1, column=0, sticky=tk.W)
        self.description_entry = tk.Entry(input_frame)
        self.description_entry.grid(row=1, column=1)

        # Amount input
        self.amount_label = tk.Label(input_frame, text="Amount")
        self.amount_label.grid(row=2, column=0, sticky=tk.W)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=2, column=1)

        # Button frame
        button_frame = tk.Frame(self.root, pady=10)
        button_frame.pack()

        self.add_button = tk.Button(button_frame, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=0, column=0, padx=5)

        self.delete_button = tk.Button(button_frame, text="Delete Expense", command=self.delete_expense)
        self.delete_button.grid(row=0, column=1, padx=5)

        self.display_button = tk.Button(button_frame, text="Display Expenses", command=self.display_expenses)
        self.display_button.grid(row=0, column=2, padx=5)

        self.save_button = tk.Button(button_frame, text="Save Expenses", command=self.save_expenses)
        self.save_button.grid(row=0, column=3, padx=5)

        # Expense display table
        self.tree = ttk.Treeview(self.root, columns=("Date", "Description", "Amount"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")
        self.tree.column("Date", minwidth=100, width=120)
        self.tree.column("Description", minwidth=100, width=150)
        self.tree.column("Amount", minwidth=50, width=80)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Initialize expense list
        self.expenses = []

    def add_expense(self):
        date = self.date_entry.get()
        description = self.description_entry.get()
        amount = self.amount_entry.get()

        # Input validation
        if not date or not description or not amount:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number!")
            return

        # Add expense to the list and table
        self.expenses.append((date, description, amount))
        self.tree.insert("", tk.END, values=(date, description, amount))

        # Clear input fields
        self.date_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Error", "No expense selected!")
            return

        for item in selected_item:
            item_data = self.tree.item(item, "values")
            self.expenses.remove(item_data)
            self.tree.delete(item)

    def display_expenses(self):
        if self.expenses:
            analyze_expenses(self.expenses)
            visualize_expenses(self.expenses)
        else:
            messagebox.showinfo("No Data", "No expenses to display.")

    def save_expenses(self):
        if not self.expenses:
            messagebox.showinfo("No Data", "No expenses to save.")
            return

        with open("expenses.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Amount"])
            writer.writerows(self.expenses)
        messagebox.showinfo("Success", "Expenses saved to expenses.csv")

# Expense analysis functions
def analyze_expenses(expenses):
    total_expenses = np.sum([expense[2] for expense in expenses])
    average_expense = np.mean([expense[2] for expense in expenses])
    print(f"Total Expenses: {total_expenses}")
    print(f"Average Expense: {average_expense}")

def visualize_expenses(expenses):
    categories = [expense[1] for expense in expenses]
    amounts = [expense[2] for expense in expenses]

    # Create pie chart
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    ax[0].set_title("Expenses by Category")

    # Create bar chart for expenses over time
    dates = [expense[0] for expense in expenses]
    ax[1].bar(dates, amounts, color='skyblue')
    ax[1].set_xlabel("Date")
    ax[1].set_ylabel("Amount")
    ax[1].set_title("Expenses Over Time")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseManager(root)
    root.mainloop()
