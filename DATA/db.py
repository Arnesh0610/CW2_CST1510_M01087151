import sqlite3
from pathlib import Path
import os
import pandas as pd
from data.schema import create_all_tables

DATA_DIR = Path("DATAS")
DB_PATH = DATA_DIR / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    #Connect to SQLite database.
    # Ensure the DATA directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Create connection
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row  # Optional: returns rows as dictionaries

    print(f"📂 Connected to database: {db_path}")

    return conn

def load_csv_to_table(conn, csv_path, table_name, date_columns=None):
    #Check if CSV file exists
    if not os.path.exists(csv_path):
        print(f" CSV file not found: {csv_path}")
        return 0

    # Check if table already has data
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    existing_rows = cursor.fetchone()[0]
    if existing_rows > 0:
        print(f"   Table {table_name} already has {existing_rows} rows. Skipping CSV load to preserve data.")
        return 0

    #Read CSV using pandas.read_csv()
    try:
        read_params = {}
        if date_columns:
            read_params['parse_dates'] = date_columns

        df = pd.read_csv(csv_path, **read_params)
        # TODO: Use df.to_sql() to insert data
        print(f"   Loading {len(df)} rows from {csv_path} into {table_name} table...")
        print(f"   Columns: {list(df.columns)}")

        # Load data into database
        # Parameters: name=table_name, con=conn, if_exists='append', index=False
        rows_loaded = df.to_sql(
            name=table_name,
            con=conn,
            if_exists='append',
            index=False
        )

        #Print success message and return row count
        print(f"✅ Successfully loaded {rows_loaded} rows into {table_name} table!")
        return rows_loaded

    except Exception as e:
        print(f"   Error loading CSV into {table_name}: {e}")
        return 0
    
def load_all_csv_data(conn):
    
    #Define CSV files and their corresponding tables
    csv_files = [
        {
            "path": DATA_DIR / "cyber_incidents.csv",
            "table": "cyber_incidents",
            "date_columns": ["timestamp"]  # Specify date columns to parse
        },
        {
            "path": DATA_DIR / "datasets_metadata.csv",
            "table": "datasets_metadata",
            "date_columns": None
        },
        {
            "path": DATA_DIR / "it_tickets.csv",
            "table": "it_tickets",
            "date_columns": ["created_at"]
        },
    ]
    #Initialize total rows loaded counter
    total_rows_loaded = 0
    
    #Load each CSV file into its corresponding table
    for csv_info in csv_files:
        csv_path = csv_info["path"]
        table_name = csv_info["table"]
        date_columns = csv_info.get("date_columns")
        #Check if CSV file exists
        if csv_path.exists():
            rows_loaded = load_csv_to_table(
                conn, 
                csv_path, 
                table_name, 
                date_columns
            )
            total_rows_loaded += rows_loaded
        else:
            print(f"⚠️  CSV file not found: {csv_path.name}")
            print(f"   Skipping {table_name} table...")
    #Print total rows loaded
    print(f"\n✅ Total rows loaded from all CSV files: {total_rows_loaded}")
    return total_rows_loaded
     
#Complete database setup function
def setup_database_complete():
    """
        Complete database setup:
        1. Connect to database
        2. Create all tables
        3. Migrate users from users.txt
        4. Load CSV data for all domains
        5. Verify setup
    """
    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)
     
    #Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("       Connected")

    #Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)

    #Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    from app.services.user_service import migrate_users_from_file
    user_count = migrate_users_from_file(conn)
    print(f"       Migrated {user_count} users")
     
    #Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    total_rows = load_all_csv_data(conn)

    #Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()

    #Count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)

    #Loop through tables and print row counts
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")

    conn.close()

    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    #Showing database location
    print(f"\n Database location: {DB_PATH.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")
