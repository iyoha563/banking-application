import pymysql
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import random

class BankingSystem:
    def __init__(self):
        self.mydb = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="isominabolism",
        )
        self.mycursor = self.mydb.cursor()
        self._initialize_database()

    def _initialize_database(self):
        self.mycursor.execute("CREATE DATABASE IF NOT EXISTS my_project")
        self.mycursor.execute("USE my_project")
        self.mycursor.execute("""
                              
            CREATE TABLE IF NOT EXISTS OPAY (
                Account_number INT PRIMARY KEY NOT NULL,
                customer_name VARCHAR(200) NOT NULL,
                dob DATE NOT NULL,
                email VARCHAR(155) UNIQUE NOT NULL,
                maiden_name VARCHAR(200) NOT NULL,
                next_kin VARCHAR(200) NOT NULL,
                address VARCHAR(200) NOT NULL,
                nin INT UNIQUE NOT NULL,
                bvn INT UNIQUE NOT NULL,
                balance INT NOT NULL,
                phone_number INT UNIQUE NOT NULL,
                transaction_history VARCHAR(1000) NOT NULL
            )
       
          """)
        

        self.mydb.commit()

    def _generate_account_number(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(10)])
    ## this return here return the value to its caller i.e another method in this same class

    def register(self):
        account_number = self._generate_account_number()
        customer_name = simpledialog.askstring("Input", "Enter name:")
        dob = simpledialog.askstring("Input", "Enter date of birth (YYYY-MM-DD):")
        email = simpledialog.askstring("Input", "Enter email address:")
        maiden_name = simpledialog.askstring("Input", "Enter maiden name:")
        next_kin = simpledialog.askstring("Input", "Enter next of kin:")
        address = simpledialog.askstring("Input", "Enter address:")
        nin = simpledialog.askstring("Input", "Enter NIN:")
        bvn = simpledialog.askstring("Input", "Enter BVN:")
        balance = 0
        phone_number = simpledialog.askstring("Input", "Enter your phone number:")
        transaction_history = ""

        query = """
            INSERT INTO OPAY (
                Account_number, customer_name, dob, email, maiden_name,
                next_kin, address, nin, bvn, balance, phone_number, transaction_history
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.mycursor.execute(query, (account_number, customer_name, dob, email, maiden_name, next_kin, address, nin, bvn, balance, phone_number, transaction_history))
        self.mydb.commit()
        messagebox.showinfo("Success", "Record inserted successfully.")

    def deposit(self):
        amount = simpledialog.askfloat("Input", "Enter amount:")
        account = simpledialog.askstring("Input", "Enter account number:")

        query = "SELECT balance FROM OPAY WHERE Account_number = %s"
        self.mycursor.execute(query, (account,))
        result = self.mycursor.fetchone()
        if result is None:
            messagebox.showerror("Error", "Account not found.")
            return

        current_balance = result[0]
        new_balance = current_balance + amount

        update_query = "UPDATE OPAY SET balance = %s WHERE Account_number = %s"
        self.mycursor.execute(update_query, (new_balance, account))
        self.mydb.commit()

        message = f"Your deposit of #{amount} is completed."
        self._update_transaction_history(account, message)
        messagebox.showinfo("Success", message)

    def transfer(self):
        amount = simpledialog.askfloat("Input", "Enter transfer amount:")
        sender_account = simpledialog.askstring("Input", "Enter your account number:")
        receiver_account = simpledialog.askstring("Input", "Enter receiver account number:")

        sender_query = "SELECT balance FROM OPAY WHERE Account_number = %s"
        self.mycursor.execute(sender_query, (sender_account,))
        sender_result = self.mycursor.fetchone()
        if sender_result is None:
            messagebox.showerror("Error", "Sender account not found.")
            return

        receiver_query = "SELECT balance FROM OPAY WHERE Account_number = %s"
        self.mycursor.execute(receiver_query, (receiver_account,))
        receiver_result = self.mycursor.fetchone()
        if receiver_result is None:
            messagebox.showerror("Error", "Receiver account not found.")
            return

        sender_balance = sender_result[0]
        receiver_balance = receiver_result[0]

        if amount > sender_balance:
            messagebox.showerror("Error", "Insufficient balance!")
            return

        new_sender_balance = sender_balance - amount
        new_receiver_balance = receiver_balance + amount

        update_sender_query = "UPDATE OPAY SET balance = %s WHERE Account_number = %s"
        self.mycursor.execute(update_sender_query, (new_sender_balance, sender_account))

        update_receiver_query = "UPDATE OPAY SET balance = %s WHERE Account_number = %s"
        self.mycursor.execute(update_receiver_query, (new_receiver_balance, receiver_account))
        self.mydb.commit()

        sender_message = f"You have been debited #{amount}."
        receiver_message = f"You have been credited #{amount}."

        self._update_transaction_history(sender_account, sender_message)
        self._update_transaction_history(receiver_account, receiver_message)
        messagebox.showinfo("Success", f"Transfer of #{amount} is successful.")

    def airtime(self):
        amount = simpledialog.askinteger("Input", "Enter airtime amount (50, 100, 200, 500, 1000):")
        phone_number = simpledialog.askstring("Input", "Enter phone number:")

        query = "SELECT balance FROM OPAY WHERE phone_number = %s"
        self.mycursor.execute(query, (phone_number,))
        result = self.mycursor.fetchone()
        if result is None:
            messagebox.showerror("Error", "Phone number not found.")
            return

        current_balance = result[0]

        if amount not in [50, 100, 200, 500, 1000]:
            messagebox.showerror("Error", "Invalid amount.")
            return

        if amount > current_balance:
            messagebox.showerror("Error", "Insufficient balance!")
            return

        new_balance = current_balance - amount
        update_query = "UPDATE OPAY SET balance = %s WHERE phone_number = %s"
        self.mycursor.execute(update_query, (new_balance, phone_number))
        self.mydb.commit()

        message = f"Your #{amount} airtime recharge is successful."
        self._update_transaction_history(phone_number, message)
        messagebox.showinfo("Success", message)

    def tv(self):
        amount = simpledialog.askinteger("Input", "Enter TV package amount (5000, 10000, 20000, 25000):")
        account_number = simpledialog.askstring("Input", "Enter your account number:")

        query = "SELECT balance FROM OPAY WHERE Account_number = %s"
        self.mycursor.execute(query, (account_number,))
        result = self.mycursor.fetchone()
        if result is None:
            messagebox.showerror("Error", "Account number not found.")
            return

        current_balance = result[0]

        if amount not in [5000, 10000, 20000, 25000]:
            messagebox.showerror("Error", "Invalid amount.")
            return

        if amount > current_balance:
            messagebox.showerror("Error", "Insufficient balance!")
            return

        new_balance = current_balance - amount
        update_query = "UPDATE OPAY SET balance = %s WHERE Account_number = %s"
        self.mycursor.execute(update_query, (new_balance, account_number))
        self.mydb.commit()

        message = f"Your #{amount} TV recharge is successful."
        self._update_transaction_history(account_number, message)
        messagebox.showinfo("Success", message)

    def _update_transaction_history(self, account, message):
        query = "SELECT transaction_history FROM OPAY WHERE Account_number = %s"
        self.mycursor.execute(query, (account,))
        result = self.mycursor.fetchone()
        current_history = result[0] if result else ""
        new_history = current_history + "\n" + message
        update_query = "UPDATE OPAY SET transaction_history = %s WHERE Account_number = %s"
        self.mycursor.execute(update_query, (new_history, account))
        self.mydb.commit()

class BankingApp(tk.Tk):
    def __init__(self, banking_system):
        super().__init__()
        self.banking_system = banking_system
        self.title("Banking System")
        self.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self, text="Register", command=self.banking_system.register).pack(pady=10)
        tk.Button(self, text="Deposit", command=self.banking_system.deposit).pack(pady=10)
        tk.Button(self, text="Transfer", command=self.banking_system.transfer).pack(pady=10)
        tk.Button(self, text="Airtime", command=self.banking_system.airtime).pack(pady=10)
        tk.Button(self, text="TV Recharge", command=self.banking_system.tv).pack(pady=10)

if __name__ == "__main__":
    banking_system = BankingSystem()
    app = BankingApp(banking_system)
    app.mainloop()