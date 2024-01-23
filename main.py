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

def render_edit_page():
    st.title("New Diary Entry")

    # Date input for the diary entry
    date = st.date_input("Date", value=datetime.today())
    date_str = date.strftime("%Y-%m-%d")

    content = st.text_area("Content", value=st.session_state.get('diary_entries', {}).get(date_str, ''), key=date_str, height=300)

    # Button to save the diary entry
    if st.button("Save Entry"):
        st.session_state.diary_entries[date_str] = content
        set_to_local_storage(TOOL_NAME, st.session_state.diary_entries)
        go_to_edit_page()

def render_diary_page():
    st.title("Diary Entries")
    for date_str, entry in sorted(st.session_state.diary_entries.items(), reverse=True):
        st.subheader(date_str)
        st.write(entry)
def render_sidebar():
    if st.sidebar.button("Diary Entries"):
        go_to_diary_page()
    if st.sidebar.button("Write New Entry"):
        go_to_edit_page()

def go_to_edit_page():
    st.session_state.edit_diary = True
    st.rerun()

def go_to_diary_page():
    st.session_state.edit_diary = False
    st.rerun()

def main():
    initialize_session()
    render_sidebar()
    if st.session_state.get('edit_diary'):
        render_edit_page()
    else:
        render_diary_page()
    st.write(st.session_state)

main()