import streamlit as st
import datetime
import matplotlib.pyplot as plt

if "logged_in" not in st.session_state:
   st.session_state.logged_in = False

# Check if user is logged in
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
        st.stop()
else:
    st.title("📊 IT Operation")

    from data.db import connect_database, setup_database_complete
    from data.tickets import get_all_tickets, insert_ticket, delete_ticket, update_ticket_status
    from data.tickets import get_tickets_by_priority_count, get_high_priority_by_status, get_ticket_priorities_with_many_cases
    
    #Connect to database (Week 8 function)
    conn = connect_database("DATAS/intelligence_platform.db")

    #Setup database if not already done
    setup_database_complete()

    st.subheader("IT tickets Dashboard")

    tickets = get_all_tickets(conn) 
    st.dataframe(tickets, use_container_width=True) 

    #Doing bar chart
    st.subheader("Bar chart to show Tickets by Priority")
    priority_counts = tickets["priority"].value_counts().reset_index()
    priority_counts.columns = ["priority", "count"]

    st.bar_chart(priority_counts.set_index("priority"))

    col3,col4 = st.columns(2)
    with col3:
        #Pie chart for assigned_to using matplotlib
        st.subheader("Pie chart to show Tickets by Assigned To")
        assigned_to_counts = tickets["assigned_to"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(assigned_to_counts, labels=assigned_to_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    with col4:
        #Line chart for status
        st.subheader("Line chart to show Tickets by Status")
        status_counts = tickets["status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]
        
        st.line_chart(status_counts.set_index("status"))


    # CREATE: Add new incident with a form
    st.markdown("Add Ticket")
    with st.form("new_ticket"):
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        description = st.text_area("Description")
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed", "Waiting For User"])
        assigned_to = st.selectbox("Assigned To", ["IT_Support_A", "IT_Support_B", "IT_Support_C"])
        date = st.date_input("Select date", datetime.date(2024, 1, 1))
        time = st.time_input("Select time", datetime.time(2, 0, 0))
        created_at = datetime.datetime.combine(date, time)
        st.write(f"Full timestamp: {created_at}")
        resolution_time_hours = st.number_input("Resolution Time (hours)", min_value=0, step=1)
        # Form submit button
        submitted = st.form_submit_button("Add Ticket")

    # When form is submitted
    if submitted:
        insert_ticket(conn, priority, description, status, assigned_to, created_at, resolution_time_hours)
        st.success("Ticket added successfully")
        st.rerun() 

    # Deleting a ticket
    st.markdown("Delete Ticket")
    with st.form("delete_ticket"):
        ticket_id = st.text_input("Enter Ticket ID to Delete")
        submit_todelete = st.form_submit_button("delete ticket")

    if (submit_todelete and ticket_id):
        delete_ticket(conn, ticket_id)
        st.success("Ticket deleted")
        st.rerun()
       
    # Updating a ticket
    st.markdown("Update Ticket Status")
    with st.form("update_ticket"):
        ticket_id_update = st.text_input("Enter Ticket ID to Update Status")
        new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved"])
        submit_toupdate = st.form_submit_button("Update Ticket Status")

    if (submit_toupdate and ticket_id_update):
        update_ticket_status(conn, ticket_id_update, new_status)
        st.success("Ticket status updated")
        st.rerun()

    # Showing Tickets by Priority
    st.subheader("Tickets by Priority")
    ticket_prioritycount= get_tickets_by_priority_count(conn)
    st.dataframe(ticket_prioritycount, use_container_width=True)

    # Showing Open Tickets by Status
    st.subheader("Open Tickets by Status")
    high_priority= get_high_priority_by_status(conn)
    st.dataframe(high_priority, use_container_width=True)

    # Showing Priorities with Many Tickets
    st.subheader("Priorities with Many Tickets")
    many_cases= get_ticket_priorities_with_many_cases(conn)
    st.dataframe(many_cases, use_container_width=True)









