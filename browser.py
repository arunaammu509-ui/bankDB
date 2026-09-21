import streamlit as st
import mysql.connector

# MySQL Connection
try:
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="1618",
        database="BANKDB"
    )
    cursor = conn.cursor()
    st.success("Connected Successfully to BANKDB")
except Exception as e:
    st.error(f"Connection Failed: {e}")
    st.stop()

st.title("Hello Streamlit!")
st.write("This is a simple interactive app.")

name = st.text_input("Enter your name")

if st.button("Greet"):
    if name.strip() == "":
        st.warning("Please enter your name")
    else:
        st.write(f"Hello, {name}! 👋")


