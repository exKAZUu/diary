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

def initialize_session():
    if 'diary_entries' not in st.session_state:
        with st.spinner():
            saved = get_from_local_storage(TOOL_NAME)
            if saved is not None:
                st.session_state.diary_entries = saved

# Navigate to the home page
def go_to_home():
    st.session_state.selected_entry = None
    st.rerun()

def render_home_page():
    st.title("New Diary Entry")

    # Date input for the diary entry
    date = st.date_input("Date", value=datetime.today())
    date_str = date.strftime("%Y-%m-%d")

    content = st.text_area("Content", value=st.session_state.get('diary_entries', {}).get(date_str, ''), key=date_str, height=300)
    # if date_str in st.session_state.diary_entries:
    #     st.session_state[date_str] = st.session_state.diary_entries[date_str]
    # else:
    #     content = st.text_area("Content", height=300)

    # Button to save the diary entry
    if st.button("Save Entry"):
        st.session_state.diary_entries[date_str] = content
        set_to_local_storage(TOOL_NAME, st.session_state.diary_entries)
        go_to_home()

def render_diary_page(date_str):
    st.title(f"Diary Entry for {date_str}")
    st.write(st.session_state.diary_entries[date_str])

def render_sidebar():
    # Sidebar layout for listing entries and navigating to the home page
    if st.sidebar.button("Write New Entry"):
        go_to_home()
    st.sidebar.header("Diary Entries")

    if 'diary_entries' in st.session_state:
        sorted_dates = sorted(st.session_state.diary_entries.keys(), reverse=True)
        for date_str in sorted_dates:
            if st.sidebar.button(f"View {date_str}"):
                st.session_state.selected_entry = date_str

def main():
    initialize_session()
    render_sidebar()
    selected_entry = st.session_state.get('selected_entry')
    if selected_entry:
        render_diary_page(selected_entry)
    else:
        render_home_page()
    st.write(st.session_state)

main()