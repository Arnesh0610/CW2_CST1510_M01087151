import streamlit as st
import datetime

if "logged_in" not in st.session_state:
   st.session_state.logged_in = False

# Check if user is logged in
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
        st.stop()
else:
    st.title("📊 Data Science")

    from data.db import connect_database, setup_database_complete
    from data.datasets import get_all_datasets, insert_dataset, delete_dataset, update_dataset_name
    from data.datasets import get_datasets_by_uploader_count, get_large_datasets_by_uploader, get_uploaders_with_many_datasets
    #Connect to database (Week 8 function)
    conn = connect_database("DATAS/intelligence_platform.db")

    #Setup database if not already done
    setup_database_complete()

    st.subheader("Datasets Dashboard")

    datasets = get_all_datasets(conn) 
    st.dataframe(datasets, use_container_width=True) 
    
    #Doing bar char
    st.subheader("Bar chart to show Datasets by Uploader")
    uploadedby_counts = datasets["uploaded_by"].value_counts().reset_index()
    uploadedby_counts.columns = ["uploaded_by", "count"]

    st.bar_chart(uploadedby_counts.set_index("uploaded_by"))

    #CREATE: Add new dataset with a form
    st.markdown("Add dataset")
    with st.form("new_dataset"):
        name= st.text_input("Name")
        rows= st.number_input("Number of Rows", min_value=0, step=1)
        columns= st.number_input("Number of Columns", min_value=0, step=1)
        uploaded_by= st.text_input("Uploaded By")
        upload_date= st.date_input("Upload Date", datetime.date.today())
        #Form submit button
        submitted = st.form_submit_button("Add dataset")

    #When form is submitted
    if submitted:
        insert_dataset(conn, name, rows, columns, uploaded_by, upload_date)
        st.success("Dataset added successfully")
        #Refresh the page to show new dataset
        st.rerun() 

    #Deleting a dataset 
    st.markdown("Delete Dataset")
    with st.form("delete_dataset"):
        dataset_id = st.text_input("Enter Dataset ID to Delete")
        submit_todelete = st.form_submit_button("delete dataset")
        
    if (submit_todelete and dataset_id):
        delete_dataset(conn, dataset_id)
        st.success("Dataset deleted")
        st.rerun()

    #Updating a dataset
    st.markdown("Update Dataset Name")
    with st.form("update_dataset"):
        dataset_id = st.text_input("Enter Dataset ID to Update")
        new_name= st.text_input("Dataset New Name")
        submit_toupdate = st.form_submit_button("update dataset")

    if (submit_toupdate and dataset_id):
        update_dataset_name(conn, dataset_id, new_name)
        st.success("Dataset deleted")
        st.rerun()

    #Showing Datasets by uploader
    st.subheader("Datasets by Uploader")
    uploader_count= get_datasets_by_uploader_count(conn)
    st.dataframe(uploader_count, use_container_width=True)

    #Showing Large Datasets by uploader
    st.subheader("Large Datasets (rows > 100) by Uploader")
    large_datasets= get_large_datasets_by_uploader(conn)
    st.dataframe(large_datasets, use_container_width=True)

    #Showing Uploaders with more than 2 datasets
    st.subheader("Uploaders with more than 2 datasets")
    uploaders_many_datasets= get_uploaders_with_many_datasets(conn, min_count=2)
    st.dataframe(uploaders_many_datasets, use_container_width=True)



