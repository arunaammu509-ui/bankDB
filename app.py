import os
import streamlit as st
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Banking System", layout="centered", page_icon="🏦")

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "BANKDB")
    )

# Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = ""
if "account_id" not in st.session_state:
    st.session_state.account_id = None
if "name" not in st.session_state:
    st.session_state.name = ""

# DB Check
try:
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'bank' AND COLUMN_NAME = 'transaction_time'
    """)
    if cursor.fetchone()[0] == 0:
        cursor.execute("ALTER TABLE bank ADD COLUMN transaction_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP")
        db.commit()
    cursor.close()
    db.close()
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.info("Check your.env file and MySQL is running")
    st.stop()

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🏦 Banking System")
    login_type = st.radio("Login Type", ["👤 User Login", "🛡️ Admin Login"], horizontal=True)

    if login_type == "👤 User Login":
        st.subheader("User Login")
        acc_no = st.number_input("Account Number", min_value=1, step=1)
        pwd = st.text_input("Login Password", type="password")
        if st.button("User Login"):
            if not pwd.strip(): st.error("Enter login password")
            else:
                db = get_db(); cur = db.cursor()
                cur.execute("SELECT name FROM bank WHERE account_id=%s AND login_password=%s ORDER BY id DESC LIMIT 1", (acc_no, pwd))
                res = cur.fetchone(); cur.close(); db.close()
                if res:
                    st.session_state.logged_in=True; st.session_state.role="user"
                    st.session_state.account_id=acc_no; st.session_state.name=res[0]
                    st.rerun()
                else: st.error("Invalid Account Number or Password")
    else:
        st.subheader("Admin Login")
        user = st.text_input("Admin Username"); pwd = st.text_input("Admin Password", type="password")
        if st.button("Admin Login"):
            if user=="admin" and pwd=="admin123":
                st.session_state.logged_in=True; st.session_state.role="admin"; st.rerun()
            else: st.error("Invalid Admin Credentials")
    st.stop()

# --- USER DASHBOARD ---
if st.session_state.role == "user":
    # (Un code same thaan, naan mathala)
    st.title("User Dashboard")
    st.sidebar.write(f"**Acc:** {st.session_state.account_id} | **Name:** {st.session_state.name}")
    menu = st.sidebar.selectbox("Menu", ["My Account", "Deposit", "Withdraw", "Balance", "Transaction Details"])

    # My Account, Deposit, Withdraw, Balance, Transaction code unathu same-a vechukalam - 100% correct
    # Copy your old logic here for those 5 menus...

    # NOTE: Paste your old My Account to Transaction Details logic here as it is.
    # For space, I am keeping Deposit/Withdraw logic same as yours.

    if menu == "My Account":
        try:
            db=get_db(); cur=db.cursor()
            cur.execute("SELECT account_id, name, balance, transaction_time FROM bank WHERE account_id=%s ORDER BY id DESC LIMIT 1", (st.session_state.account_id,))
            r=cur.fetchone(); cur.close(); db.close()
            if r:
                st.write(f"Account Number: {r[0]}"); st.write(f"Holder: {r[1]}")
                st.success(f"Current Balance: {float(r[2]):.2f}")
                st.write(f"Last Transaction: {r[3].strftime('%d-%m-%Y %I:%M:%S %p')}")
        except Exception as e: st.error(str(e))

    if st.sidebar.button("Logout"):
        st.session_state.logged_in=False; st.rerun()

# --- ADMIN DASHBOARD ---
elif st.session_state.role == "admin":
    st.title("Admin Dashboard")
    menu = st.sidebar.selectbox("Admin Menu", ["Create Account", "All Bank Accounts", "All Transactions", "Delete Account"])
    # Your Admin logic is already perfect, same-a use pannalam
    if st.sidebar.button("Log out"):
        st.session_state.logged_in=False; st.rerun()
