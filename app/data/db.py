import sqlite3
from pathlib import Path
import os
import pandas as pd
from app.data.schema import create_all_tables, load_all_csv_data
from app.services.user_service import migrate_users_from_file

DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""
     

    return sqlite3.connect(str(db_path))

def load_csv_to_table(conn, csv_path, table_name, date_columns=None):
    """
    Load a CSV file into a database table using pandas.

    TODO: Implement this function.

    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table

    Returns:
        int: Number of rows loaded
    """
    # TODO: Check if CSV file exists

    # TODO: Read CSV using pandas.read_csv()

    # TODO: Use df.to_sql() to insert data
    # Parameters: name=table_name, con=conn, if_exists='append', index=False

    # TODO: Print success message and return row count

    if not os.path.exists(csv_path):
        print(f" CSV file not found: {csv_path}")
        return 0

    try:
        read_params = {}
        if date_columns:
            read_params['parse_dates'] = date_columns
            
        df = pd.read_csv(csv_path, **read_params)
        
        print(f"   Loading {len(df)} rows from {csv_path} into {table_name} table...")
        print(f"   Columns: {list(df.columns)}")
        
        # Load data into database
        rows_loaded = df.to_sql(
            name=table_name, 
            con=conn, 
            if_exists='append', 
            index=False
        )
        
        print(f"✅ Successfully loaded {rows_loaded} rows into {table_name} table!")
        return rows_loaded
        
    except Exception as e:
        print(f"   Error loading CSV into {table_name}: {e}")
        return 0
    

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

    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("       Connected")

    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)

    # Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file(conn)
    print(f"       Migrated {user_count} users")

    # Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    total_rows = load_all_csv_data(conn)

    # Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()

    # Count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")

    conn.close()

    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n Database location: {DB_PATH.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")

# Run the complete setup
setup_database_complete()