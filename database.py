import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()
print("Connected Successfully")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bank (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    login_password VARCHAR(100) NOT NULL,
    deposit_pin VARCHAR(10) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    balance DECIMAL(10,2) NOT NULL,
    transaction_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

while True:
    print("\n===== BANK MENU =====")
    print("1. Create Account")
    print("2. View Accounts")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Transaction Details")
    print("6. Delete Account")
    print("7. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter name: ")
        login_pass = input("Enter Login Password: ")
        pin = input("Enter 4-digit Deposit PIN: ")
        if name.strip() == "" or login_pass.strip() == "" or len(pin)!=4 or not pin.isdigit():
            print("Invalid input! Name/Pass empty or PIN not 4-digit")
            continue
        cursor.execute("SELECT MAX(account_id) FROM bank")
        result = cursor.fetchone()
        account_id = 1 if result[0] is None else result[0] + 1
        opening_balance = 1000.00
        cursor.execute("INSERT INTO bank (account_id, name, login_password, deposit_pin, transaction_type, amount, balance, transaction_time) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())", (account_id, name, login_pass, pin, "Opening", opening_balance, opening_balance))
        conn.commit()
        print(f"\nAccount Created! ID: {account_id}, Balance: {opening_balance}")

    elif choice == "2":
        cursor.execute("SELECT account_id, name, balance, transaction_time FROM bank WHERE id IN (SELECT MAX(id) FROM bank GROUP BY account_id) ORDER BY account_id")
        rows = cursor.fetchall()
        if not rows: print("\nNo Accounts Found")
        else:
            print("\n===== ACCOUNTS =====")
            for row in rows: print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")

    elif choice == "3":
        try:
            account_id = int(input("Enter Account ID: "))
            amount = float(input("Enter Deposit Amount: "))
            pin = input("Enter Deposit PIN: ")
        except: print("Invalid input"); continue
        if amount <=0: print("Amount >0"); continue
        cursor.execute("SELECT name, login_password, deposit_pin, balance FROM bank WHERE account_id=%s ORDER BY id DESC LIMIT 1", (account_id,))
        result = cursor.fetchone()
        if not result: print("Account not found")
        elif str(result[2])!=pin: print("Invalid PIN")
        else:
            new_balance = float(result[3]) + amount
            cursor.execute("INSERT INTO bank (account_id, name, login_password, deposit_pin, transaction_type, amount, balance, transaction_time) VALUES (%s,%s,%s,%s,%s,%s,%s,NOW())", (account_id, result[0], result[1], result[2], "Deposit", amount, new_balance))
            conn.commit()
            print(f"Deposited! New Balance: {new_balance}")

    elif choice == "4":
        try:
            account_id = int(input("Enter Account ID: "))
            amount = float(input("Enter Withdraw Amount: "))
            pin = input("Enter Deposit PIN: ")
        except: print("Invalid input"); continue
        if amount <=0: print("Amount >0"); continue
        cursor.execute("SELECT name, login_password, deposit_pin, balance FROM bank WHERE account_id=%s ORDER BY id DESC LIMIT 1", (account_id,))
        result = cursor.fetchone()
        if not result: print("Account not found")
        elif str(result[2])!=pin: print("Invalid PIN")
        elif amount > float(result[3]): print("Insufficient Balance")
        else:
            new_balance = float(result[3]) - amount
            cursor.execute("INSERT INTO bank (account_id, name, login_password, deposit_pin, transaction_type, amount, balance, transaction_time) VALUES (%s,%s,%s,%s,%s,%s,%s,NOW())", (account_id, result[0], result[1], result[2], "Withdraw", amount, new_balance))
            conn.commit()
            print(f"Withdrawn! New Balance: {new_balance}")

    elif choice == "5":
        try: account_id = int(input("Enter Account ID: "))
        except: print("Invalid ID"); continue
        cursor.execute("SELECT id, transaction_type, amount, balance, transaction_time FROM bank WHERE account_id=%s ORDER BY id", (account_id,))
        rows = cursor.fetchall()
        if not rows: print("No transactions")
        else:
            for row in rows: print(row)

    elif choice == "6":
        try: account_id = int(input("Enter Account ID: "))
        except: print("Invalid ID"); continue
        cursor.execute("DELETE FROM bank WHERE account_id=%s", (account_id,))
        if cursor.rowcount>0: conn.commit(); print("Deleted")
        else: print("Not found")

    elif choice == "7":
        print("Thank You!"); break
    else: print("Invalid Choice")

cursor.close()
conn.close()
print("Connection Closed")
