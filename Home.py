#Import necessary modules
import streamlit as st
from app.services.user_service import login_user, register_user
from data.users import get_user_by_username
from data.db import setup_database_complete

st.title("Welcome to Streamlit App")

#Create tabs for Login and Registration
tab_login, tab_register = st.tabs([
"Login", "Register"
 ])

#Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# If already logged in
if st.session_state.logged_in:
    st.success(f"Already logged in as {st.session_state.username}.")
    #Create navigation buttons:
    if st.button("Go to CyberSecurity"):
        st.switch_page("pages/CyberSecurity.py")

    if st.button("Go to Data Science"):
        st.switch_page("pages/Data_Science.py")

    if st.button("Go to IT Operation"):
        st.switch_page("pages/IT_Operation.py")

    st.divider()

    #Creating logout button
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.info("You have been logged out")
        st.switch_page("Home.py")

    st.stop()


with tab_login:

    login_username = st.text_input(
    "Username", key="login_username"
    )

    login_password = st.text_input(
    "Password", type="password",
    key="login_password"
    )

    if st.button("Log in"):
        # Check credentials
        success, message = login_user(login_username, login_password)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success(f"{login_username}, Logged in successfully!")
            st.switch_page("pages/CyberSecurity.py")   
        else:
            st.error("Invalid credentials")



with tab_register:
    st.subheader("Register")

    #Input widgets
    new_username = st.text_input(
    "Choose a username", key="register_username")
    new_password = st.text_input(
    "Choose a password", type="password",
    key="register_password")
    confirm_password = st.text_input(
    "Confirm password", type="password",
    key="register_confirm")
    role = st.selectbox(
    "Select Role", ["user", "admin", "analyst"], key="register_role")

    #Validation and registration of new user:
    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif get_user_by_username(new_username):
            st.error("Username already exists. Please choose another.")
        else:
            register_user(new_username, new_password, role)
            st.success("Account created! 🎉")
            st.info("Go to Login tab to sign in.")

# Setup database if not already done
setup_database_complete()




