#Import necessary modules
import streamlit as st
import datetime
import matplotlib.pyplot as plt
#Import database functions
from data.db import connect_database, setup_database_complete
from data.incidents import get_all_incidents, insert_incident, delete_incident, update_incident_status
from data.incidents import get_incidents_by_type_count, get_high_severity_by_status, get_incident_types_with_many_cases
    
#Checking if user is logged in
if "logged_in" not in st.session_state:
   st.session_state.logged_in = False

#When user is not logged in:
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
        st.stop()
else:
    #When user is logged in:
    st.title("📊 Cyber Security")
    
    
    #Connect to database (Week 8 function)
    conn = connect_database("DATAS/intelligence_platform.db")

    #Setup database if not already done
    setup_database_complete()

    #Page title
    st.subheader("Cyber Incidents Dashboard")

    incidents = get_all_incidents()
    st.dataframe(incidents, use_container_width=True)
    
    col1,col2 = st.columns(2)

    #Displaying metrics
    with col1:
        st.metric("High", incidents[incidents["severity"] == "High"].shape[0])
    with col2:
        st.metric("Incidents", incidents["severity"].count())
   
    #Doing bar char
    st.subheader("Bar chart to show Incidents by Severity")  
    severity_counts = incidents["severity"].value_counts().reset_index()
    severity_counts.columns = ["severity", "count"]

    st.bar_chart(severity_counts.set_index("severity"))

    col3,col4 = st.columns(2)
    with col3:
        #Pie chart for category using matplotlib
        st.subheader("Pie chart to show Incidents by Category")
        category_counts = incidents["category"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    with col4:
        #Area chart for status
        st.subheader("Area chart to show Incidents by Status")
        status_counts = incidents["status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]
        
        st.area_chart(status_counts.set_index("status"))

    # CREATE: Add new incident with a form
    st.markdown("Add Incidents")
    with st.form("new_incident"):
        #Form inputs (Streamlit widgets)
        date = st.date_input("Select date", datetime.date(2024, 1, 1))
        time = st.time_input("Select time", datetime.time(2, 0, 0))
        timestamp = datetime.datetime.combine(date, time)
        st.write(f"Full timestamp: {timestamp}")
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        category = st.selectbox("Category", ["Phishing", "Malware", "DDoS","Unauthorized Access", "Misconfiguration"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved, Closed"])
        description = st.text_input("Description")
        # Form submit button
        submitted = st.form_submit_button("Add Incident")

    # When form is submitted
    if submitted:
        insert_incident(conn, timestamp, severity, category, status, description)
        st.success(f"Incident added successfully")
        # Refresh the page to show new incident
        st.rerun()
        
    #Deleting an incident 
    st.markdown("Delete Incident")
    with st.form("delete_incident"):
        incident_id = st.text_input("Enter Incident ID to Delete")
        submit_todelete = st.form_submit_button("delete Incident")
        
    if submit_todelete:
        delete_incident(conn, incident_id)
        st.success("Incident deleted")
        st.rerun()

    #Updating an incident
    st.markdown("Update Incident Status")
    with st.form("update_incident"):
        incident_id = st.text_input("Enter Incident Id to Update")
        new_status = st.selectbox("New Status",["Open", "In Progress", "Resolved", "Closed"])
        submit_toupdate = st.form_submit_button("Update Status")

    if (submit_toupdate and incident_id):
        update_incident_status(conn,incident_id,new_status)
        st.success("Status updated")
        st.rerun

    #Showing Incident Count by Type
    st.subheader("Incident Count by Type")
    incident_typecount= get_incidents_by_type_count(conn)
    st.dataframe(incident_typecount, use_container_width=True)

    #Showing High Severity Incidents by Status
    st.subheader("High Severity Incidents by Status")
    highseverity_incident= get_high_severity_by_status(conn)
    st.dataframe(highseverity_incident, use_container_width=True)

    #Showing Incident Types with Many Cases
    st.subheader("Incident Types with Many Cases(More than 5)")
    incident_mincase= get_incident_types_with_many_cases(conn)
    st.dataframe(incident_mincase, use_container_width=True)
