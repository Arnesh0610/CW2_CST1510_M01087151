import pandas as pd
from app.data.db import connect_database

def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """
    Insert a new cyber incident into the database.

    TODO: Implement this function following the register_user() pattern.

    Args:
        conn: Database connection
        date: Incident date (YYYY-MM-DD)
        incident_type: Type of incident
        severity: Severity level
        status: Current status
        description: Incident description
        reported_by: Username of reporter (optional)

    Returns:
        int: ID of the inserted incident
    """
    # Get cursor
    cursor = conn.cursor()
    
    # Write INSERT SQL with parameterized query
    sql = """
        INSERT INTO incidents (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    
    # Execute and commit
    cursor.execute(sql, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    
    # Return cursor.lastrowid
    return cursor.lastrowid

def get_all_incidents(conn):
    import pandas as pd
    """
    Retrieve all incidents from the database.

    Returns:
        pandas.DataFrame: All incidents
    """
    # Use pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    
    return pd.read_sql_query("SELECT * FROM cyber_incidents", conn)

def update_incident_status(conn, incident_id, new_status):
    """
    Update the status of an incident.

    Args:
        conn: Database connection
        incident_id: ID of the incident to update
        new_status: New status value

    Returns:
        int: Number of rows affected (should be 1 if successful)
    """
    # Write UPDATE SQL: UPDATE cyber_incidents SET status = ? WHERE id = ?
    cursor = conn.cursor()
    sql = "UPDATE cyber_incidents SET status = ? WHERE id = ?"
    
    # Execute and commit
    cursor.execute(sql, (new_status, incident_id))
    conn.commit()
    
    # Return cursor.rowcount
    return cursor.rowcount

def delete_incident(conn, incident_id):
    """
    Delete an incident from the database.

    Args:
        conn: Database connection
        incident_id: ID of the incident to delete

    Returns:
        int: Number of rows affected (should be 1 if successful)
    """
    # Write DELETE SQL: DELETE FROM cyber_incidents WHERE id = ?
    cursor = conn.cursor()
    sql = "DELETE FROM cyber_incidents WHERE id = ?"
    
    # Execute and commit
    cursor.execute(sql, (incident_id,))
    conn.commit()
    
    # Return cursor.rowcount
    return cursor.rowcount


def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
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
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

# Test: Run analytical queries
conn = connect_database()

print("\n Incidents by Type:")
df_by_type = get_incidents_by_type_count(conn)
print(df_by_type)

print("\n High Severity Incidents by Status:")
df_high_severity = get_high_severity_by_status(conn)
print(df_high_severity)

print("\n Incident Types with Many Cases (>5):")
df_many_cases = get_incident_types_with_many_cases(conn, min_count=5)
print(df_many_cases)

conn.close()
    