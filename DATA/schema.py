#Create database schema: tables and their structure:
#Create users table
def create_users_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    print("✅ Users table created successfully!")

#Create cyber incidents table
def create_cyber_incidents_table(conn):
    cursor=conn.cursor()

    #Write CREATE TABLE IF NOT EXISTS SQL statement
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            severity TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT
        )
    """)

    #Commit the changes
    conn.commit()

    #Print success message
    print("Cyber incidents table created successfully!")

#Create datasets metadata table
def create_datasets_metadata_table(conn):

    cursor=conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS datasets_metadata")

    cursor.execute("""
    CREATE TABLE datasets_metadata (
        dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rows INTEGER NOT NULL,
        columns INTEGER NOT NULL,
        uploaded_by TEXT NOT NULL,
        upload_date TEXT NOT NULL
    )
    """)

    conn.commit()
    print("Datasets metadata table created successfully!")

#Create IT tickets table
def create_it_tickets_table(conn):
    cursor=conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS it_tickets")

    cursor.execute("""
        CREATE TABLE it_tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            priority TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            assigned_to TEXT,
            created_at TEXT NOT NULL,
            resolution_time_hours INTEGER
        )
        """)

    conn.commit()
    print("IT tickets table created successfully!")

#Create all tables
def create_all_tables(conn):
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)