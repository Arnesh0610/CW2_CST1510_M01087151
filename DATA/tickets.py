#Import necessary modules
import pandas as pd
from data.db import connect_database

#Function to get all tickets
def get_all_tickets(conn):
    #Get all tickets as DataFrame.
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY ticket_id",
        conn
    )
    return df

#Function to insert a new ticket
def insert_ticket(conn, priority, description, status, assigned_to, created_at, resolution_time_hours):

    # Get cursor
    cursor = conn.cursor()

    #Write INSERT SQL with parameterized query
    sql = """
        INSERT INTO it_tickets (priority, description, status, assigned_to, created_at, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    # Execute and commit
    cursor.execute(sql, (priority, description, status, assigned_to, created_at, resolution_time_hours))
    conn.commit()

    # Return cursor.lastrowid
    return  cursor.lastrowid

#Function to update ticket status
def update_ticket_status(conn, ticket_id, new_status):
    # Write UPDATE SQL: UPDATE it_tickets SET status = ? WHERE ticket_id = ?
    cursor = conn.cursor()
    sql = "UPDATE it_tickets SET status = ? WHERE ticket_id = ?"

    # Execute and commit
    cursor.execute(sql, (new_status, ticket_id))
    conn.commit()

    # Return cursor.rowcount
    return cursor.rowcount

#Function to delete a ticket
def delete_ticket(conn, ticket_id):
    # Write DELETE SQL: DELETE FROM it_tickets WHERE ticket_id = ?
    cursor = conn.cursor()
    sql = "DELETE FROM it_tickets WHERE ticket_id = ?"

    # Execute and commit
    cursor.execute(sql, (ticket_id,))
    conn.commit()

    # Return cursor.rowcount
    return cursor.rowcount

#Analytical query functions for IT tickets
def get_tickets_by_priority_count(conn):
    query = """
    SELECT priority, COUNT(*) as count
    FROM it_tickets
    GROUP BY priority
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

#Function to get high priority tickets by status
def get_high_priority_by_status(conn):
    query = """
    SELECT status, COUNT(*) as count
    FROM it_tickets
    WHERE priority = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

#Function to get ticket priorities with many cases
def get_ticket_priorities_with_many_cases(conn, min_count=5):
    query = """
    SELECT priority, COUNT(*) as count
    FROM it_tickets
    GROUP BY priority
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

#Test: Run analytical queries
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
