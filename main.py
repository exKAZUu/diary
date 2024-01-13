import json
import time
import streamlit as st
from streamlit_javascript import st_javascript
from datetime import datetime

TOOL_NAME = 'simulation-diary'

def get_from_local_storage(key):
    value = st_javascript(
        f"JSON.parse(localStorage.getItem('{key}')) || {{}}"
    )
    return value if value != 0 else None


def set_to_local_storage(key, value):
    jdata = json.dumps(value)
    st_javascript(
        f"localStorage.setItem('{key}', JSON.stringify({jdata}));"
    )
    # Wait for saving data to the local storage
    time.sleep(0.5)


# Initialize session state for diary entries and selected entry
if 'diary_entries' not in st.session_state:
    with st.spinner():
        saved = get_from_local_storage(TOOL_NAME)
        print('load', saved)
        if saved is not None:
            st.session_state.diary_entries = saved

st.write(st.session_state)

# Navigate to the home page
def go_to_home():
    st.session_state.selected_entry = None
    st.rerun()

# Function to save the diary entry in session state
def save_diary_entry(date, content):
    date_str = date.strftime("%Y-%m-%d")
    st.session_state.diary_entries[date_str] = content
    set_to_local_storage(TOOL_NAME, st.session_state.diary_entries)
    go_to_home()

# Display the home page with the new entry form
def home_page():
    st.title("New Diary Entry")

    # Date input for the diary entry
    date = st.date_input("Date", value=datetime.today())

    # Text area for the diary content
    content = st.text_area("Content", height=300)

    # Button to save the diary entry
    if st.button("Save Entry"):
        save_diary_entry(date, content)

# Sidebar layout for listing entries and navigating to the home page
if st.sidebar.button("Write New Entry"):
    go_to_home()
st.sidebar.header("Diary Entries")

if 'diary_entries' in st.session_state:
    sorted_dates = sorted(st.session_state.diary_entries.keys(), reverse=True)
    for date_str in sorted_dates:
        if st.sidebar.button(f"View {date_str}"):
            st.session_state.selected_entry = date_str

def view_diary_entry(date_str):
    st.title(f"Diary Entry for {date_str}")
    st.write(st.session_state.diary_entries[date_str])

# Main page layout
selected_entry = st.session_state.get('selected_entry')
if selected_entry:
    view_diary_entry(selected_entry)
else:
    home_page()
