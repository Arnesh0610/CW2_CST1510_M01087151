import pandas as pd
from data.db import connect_database

def get_all_tickets():
    """Get all tickets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY ticket_id DESC",
        conn
    )
    conn.close()
    return df

def insert_ticket(conn, priority, description, status, assigned_to, created_at, resolution_time_hours):
    """
    Insert a new IT ticket into the database.

    Args:
        conn: Database connection
        priority: Priority level
        description: Ticket description
        status: Current status
        assigned_to: Assigned person
        created_at: Creation timestamp
        resolution_time_hours: Resolution time in hours

    Returns:
        str: ID of the inserted ticket
    """
    # Get cursor
    cursor = conn.cursor()

    # Write INSERT SQL with parameterized query
    sql = """
        INSERT INTO it_tickets (priority, description, status, assigned_to, created_at, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    # Execute and commit
    cursor.execute(sql, (priority, description, status, assigned_to, created_at, resolution_time_hours))
    conn.commit()

    # Return cursor.lastrowid
    return cursor.lastrowid

def get_all_tickets(conn):
    import pandas as pd
    """
    Retrieve all tickets from the database.

    Returns:
        pandas.DataFrame: All tickets
    """
    # Use pd.read_sql_query("SELECT * FROM it_tickets", conn)

    return pd.read_sql_query("SELECT * FROM it_tickets", conn)

def update_ticket_status(conn, ticket_id, new_status):
    """
    Update the status of a ticket.

    Args:
        conn: Database connection
        ticket_id: ID of the ticket to update
        new_status: New status value

    Returns:
        int: Number of rows affected (should be 1 if successful)
    """
    # Write UPDATE SQL: UPDATE it_tickets SET status = ? WHERE ticket_id = ?
    cursor = conn.cursor()
    sql = "UPDATE it_tickets SET status = ? WHERE ticket_id = ?"

    # Execute and commit
    cursor.execute(sql, (new_status, ticket_id))
    conn.commit()

    # Return cursor.rowcount
    return cursor.rowcount

def delete_ticket(conn, ticket_id):
    """
    Delete a ticket from the database.

    Args:
        conn: Database connection
        ticket_id: ID of the ticket to delete

    Returns:
        int: Number of rows affected (should be 1 if successful)
    """
    # Write DELETE SQL: DELETE FROM it_tickets WHERE ticket_id = ?
    cursor = conn.cursor()
    sql = "DELETE FROM it_tickets WHERE ticket_id = ?"

    # Execute and commit
    cursor.execute(sql, (ticket_id,))
    conn.commit()

    # Return cursor.rowcount
    return cursor.rowcount

def get_tickets_by_priority_count(conn):
    """
    Count tickets by priority.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT priority, COUNT(*) as count
    FROM it_tickets
    GROUP BY priority
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_priority_by_status(conn):
    """
    Count high priority tickets by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM it_tickets
    WHERE priority = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_ticket_priorities_with_many_cases(conn, min_count=5):
    """
    Find ticket priorities with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT priority, COUNT(*) as count
    FROM it_tickets
    GROUP BY priority
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

# Test: Run analytical queries
conn = connect_database()

print("\n Tickets by Priority:")
df_by_priority = get_tickets_by_priority_count(conn)
print(df_by_priority)

print("\n High Priority Tickets by Status:")
df_high_priority = get_high_priority_by_status(conn)
print(df_high_priority)

print("\n Ticket Priorities with Many Cases (>5):")
df_many_cases = get_ticket_priorities_with_many_cases(conn, min_count=5)
print(df_many_cases)

conn.close()
