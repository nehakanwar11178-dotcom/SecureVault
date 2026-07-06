import streamlit as st
import sqlite3
import os

st.title("🔐 SecureVault")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "securevault.db")

conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT,
    username TEXT,
    password TEXT
)
""")
conn.commit()

website = st.text_input("Website")
username = st.text_input("Username")
password = st.text_input("Password")

if st.button("Save Password"):
    if website and username and password:
        cursor.execute(
            "INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
            (website, username, password)
        )
        conn.commit()
        st.success("Saved Successfully!")
    else:
        st.error("Fill all fields")

st.divider()

st.subheader("Saved Data")

cursor.execute("SELECT website, username, password FROM passwords")
rows = cursor.fetchall()

for r in rows:
    st.write(f"{r[0]} | {r[1]} | {r[2]}")

