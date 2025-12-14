#Importing necessary modules
import pandas as pd
from data.db import connect_database
from data.schema import create_all_tables
from data.db import load_all_csv_data

#Function to get all incidents
def get_all_incidents():
    conn = connect_database()
    #Get all incidents as DataFrame.
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY incident_id",
        conn
    )
    conn.close()
    return df

#Insert new incident.
def insert_incident(conn, timestamp, severity, category, status, description):
    
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents
        ( timestamp, severity, category, status, description)
        VALUES ( ?, ?, ?, ?, ?)
    """, (timestamp, severity, category, status, description))
    conn.commit()

    
    return cursor.lastrowid

def update_incident_status(conn, incident_id, new_status):

    #Write UPDATE SQL: UPDATE cyber_incidents SET status = ? WHERE incident_id = ?
    cursor = conn.cursor()
    sql = "UPDATE cyber_incidents SET status = ? WHERE incident_id = ?"

    #Execute and commit
    cursor.execute(sql, (new_status, incident_id))
    conn.commit()

    #Return cursor.rowcount
    return cursor.rowcount

def delete_incident(conn, incident_id):
    #Write DELETE SQL: DELETE FROM cyber_incidents WHERE incident_id = ?
    cursor = conn.cursor()
    sql = "DELETE FROM cyber_incidents WHERE incident_id = ?"

    #Execute and commit
    cursor.execute(sql, (incident_id,))
    conn.commit()

    #Return cursor.rowcount
    return cursor.rowcount

#Analytical query functions:
def get_incidents_by_type_count(conn):
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


def get_high_severity_by_status(conn):
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_incident_types_with_many_cases(conn, min_count=5):
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

#Test: Run analytical queries
conn = connect_database()
create_all_tables(conn)
load_all_csv_data(conn)

print("\n Incidents by Type:")
df_by_type = get_incidents_by_type_count(conn)
print(df_by_type)

print("\n High Severity Incidents by Status:")
df_high_severity = get_high_severity_by_status(conn)
print(df_high_severity)

print("\n Incident Types with Many Cases (>5):")
df_many_cases = get_incident_types_with_many_cases(conn, min_count=5)
print(df_many_cases)

#Close connection
conn.close()
    