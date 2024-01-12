import streamlit as st
from datetime import datetime

# Retrieve entries from session state, or initialize an empty dictionary
if 'diary_entries' not in st.session_state:
    st.session_state.diary_entries = {}

# Streamlit app layout
st.title("My Streamlit Diary")

# Date input for the diary entry
date = st.date_input("Date")

# Text area for the diary content
content = st.text_area("Content", height=300)

# Function to save the diary entry to the session state
def save_diary_entry(date, content):
    date_str = date.strftime("%Y-%m-%d")
    st.session_state.diary_entries[date_str] = content

# Button to save the diary entry
if st.button("Save Entry"):
    save_diary_entry(date, content)
    st.success("Diary entry saved!")

# Display past entries (if any)
st.write("## Past Diary Entries")
for date, entry in sorted(st.session_state.diary_entries.items(), reverse=True):
    st.write(f"### {date}")
    st.write(entry)
    st.write("---")