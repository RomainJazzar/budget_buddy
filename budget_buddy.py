import tkinter as tk
from tkinter import messagebox, ttk
from user_manager import UserManager
from transaction_manager import TransactionManager
import datetime

class BudgetBuddyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Buddy")
        self.user_manager = UserManager()
        self.transaction_manager = TransactionManager()
        self.current_user = None
        self.show_login()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_frame()
        tk.Label(self.root, text="Login").pack()
        tk.Label(self.root, text="Email").pack()
        self.entry_email = tk.Entry(self.root)
        self.entry_email.pack()
        tk.Label(self.root, text="Password").pack()
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack()
        tk.Button(self.root, text="Login", command=self.login).pack()
        tk.Button(self.root, text="Register", command=self.show_register).pack()

    def show_register(self):
        self.clear_frame()
        tk.Label(self.root, text="Register").pack()
        tk.Label(self.root, text="Nom").pack()
        self.entry_nom = tk.Entry(self.root)
        self.entry_nom.pack()
        tk.Label(self.root, text="Prénom").pack()
        self.entry_prenom = tk.Entry(self.root)
        self.entry_prenom.pack()
        tk.Label(self.root, text="Email").pack()
        self.entry_email_reg = tk.Entry(self.root)
        self.entry_email_reg.pack()
        tk.Label(self.root, text="Password").pack()
        self.entry_password_reg = tk.Entry(self.root, show="*")
        self.entry_password_reg.pack()
        tk.Button(self.root, text="Register", command=self.register).pack()
        tk.Button(self.root, text="Back", command=self.show_login).pack()

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        user_id = self.user_manager.login(email, password)
        if user_id:
            self.current_user = user_id
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        email = self.entry_email_reg.get()
        password = self.entry_password_reg.get()
        result = self.user_manager.register(nom, prenom, email, password)
        messagebox.showinfo("Result", result)
        if "successful" in result:
            self.show_login()

    def show_dashboard(self):
        self.clear_frame()
        balance = self.transaction_manager.get_balance(self.current_user)
        tk.Label(self.root, text=f"Current Balance: {balance} €").pack()
        if balance < 0:
            messagebox.showwarning("Alert", "Your balance is negative!")
        
        tk.Button(self.root, text="Add Transaction", command=self.show_add_transaction).pack()
        tk.Button(self.root, text="View History", command=self.show_history).pack()

    def show_add_transaction(self):
        self.clear_frame()
        tk.Label(self.root, text="Add Transaction").pack()
        tk.Label(self.root, text="Reference").pack()
        ref = tk.Entry(self.root)
        ref.pack()
        tk.Label(self.root, text="Description").pack()
        desc = tk.Entry(self.root)
        desc.pack()
        tk.Label(self.root, text="Amount").pack()
        amount = tk.Entry(self.root)
        amount.pack()
        tk.Label(self.root, text="Date (YYYY-MM-DD)").pack()
        date = tk.Entry(self.root)
        date.pack()
        tk.Label(self.root, text="Type").pack()
        type_var = tk.StringVar(value="deposit")
        tk.OptionMenu(self.root, type_var, "deposit", "withdrawal", "transfer").pack()
        tk.Label(self.root, text="Category").pack()
        cat_var = tk.StringVar(value="1")
        tk.OptionMenu(self.root, cat_var, "1", "2", "3", "4", "5").pack()  # Simplified category IDs
        tk.Button(self.root, text="Save", command=lambda: self.transaction_manager.add_transaction(
            ref.get(), desc.get(), float(amount.get()), date.get(), type_var.get(), self.current_user, int(cat_var.get())
        )).pack()
        tk.Button(self.root, text="Back", command=self.show_dashboard).pack()

    def show_history(self):
        self.clear_frame()
        filters = {'order': 'ASC'}  # Example filter, expand as needed
        transactions = self.transaction_manager.get_transactions(self.current_user, filters)
        for trans in transactions:
            tk.Label(self.root, text=str(trans)).pack()
        tk.Button(self.root, text="Back", command=self.show_dashboard).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetBuddyApp(root)
    root.mainloop()