import streamlit as st

st.set_page_config(
    page_title="Student App", #<------- Change this to the page you're currently on when copying/pasting after your imports
    page_icon="⛰️",
    menu_items={
        'About': """This is an app developed by Joshua Lewis at Coding Temple. Here are our
        Github accounts : https://github.com/TechNTalk,"""} #<------- Change this to the page you're currently on when copying/pasting after your imports
)
st.title("School Directory")
st.subheader("Student Directory")
st.text("Queries and returns all information based on selected students.")