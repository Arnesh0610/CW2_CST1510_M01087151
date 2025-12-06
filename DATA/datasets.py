import pandas as pd
from data.db import connect_database

def get_all_datasets():
    """Get all datasets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY dataset_id DESC",
        conn
    )
    conn.close()
    return df

def insert_dataset(conn, name, rows, columns, uploaded_by, upload_date):
    """
    Insert a new dataset into the database.

    Args:
        conn: Database connection
        name: Dataset name
        rows: Number of rows
        columns: Number of columns
        uploaded_by: Uploader name
        upload_date: Upload date

    Returns:
        int: ID of the inserted dataset
    """
    # Get cursor
    cursor = conn.cursor()

    # Write INSERT SQL with parameterized query
    sql = """
        INSERT INTO datasets_metadata (name, rows, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?)
    """

    # Execute and commit
    cursor.execute(sql, (name, rows, columns, uploaded_by, upload_date))
    conn.commit()

    # Return cursor.lastrowid
    return cursor.lastrowid

def get_all_datasets(conn):
    import pandas as pd
    """
    Retrieve all datasets from the database.

    Returns:
        pandas.DataFrame: All datasets
    """
    # Use pd.read_sql_query("SELECT * FROM datasets_metadata", conn)

    return pd.read_sql_query("SELECT * FROM datasets_metadata", conn)

def update_dataset_name(conn, dataset_id, new_name):
    """
    Update the name of a dataset.

    Args:
        conn: Database connection
        dataset_id: ID of the dataset to update
        new_name: New name value

    Returns:
        int: Number of rows affected (should be 1 if successful)
    """
    # Write UPDATE SQL: UPDATE datasets_metadata SET name = ? WHERE dataset_id = ?
    cursor = conn.cursor()
    sql = "UPDATE datasets_metadata SET name = ? WHERE dataset_id = ?"

    # Execute and commit
    cursor.execute(sql, (new_name, dataset_id))
    conn.commit()

    # Return cursor.rowcount
    return cursor.rowcount

def delete_dataset(conn, dataset_id):
    """
    Delete a dataset from the database.

    Args:
        conn: Database connection
        dataset_id: ID of the dataset to delete

    Returns:
        int: Number of rows affected (should be 1 if successful)
    """
    # Write DELETE SQL: DELETE FROM datasets_metadata WHERE dataset_id = ?
    cursor = conn.cursor()
    sql = "DELETE FROM datasets_metadata WHERE dataset_id = ?"

    # Execute and commit
    cursor.execute(sql, (dataset_id,))
    conn.commit()

    # Return cursor.rowcount
    return cursor.rowcount

def get_datasets_by_uploader_count(conn):
    """
    Count datasets by uploader.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT uploaded_by, COUNT(*) as count
    FROM datasets_metadata
    GROUP BY uploaded_by
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_large_datasets_by_uploader(conn):
    """
    Count large datasets (rows > 100) by uploader.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT uploaded_by, COUNT(*) as count
    FROM datasets_metadata
    WHERE rows > 100
    GROUP BY uploaded_by
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_uploaders_with_many_datasets(conn, min_count=2):
    """
    Find uploaders with more than min_count datasets.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT uploaded_by, COUNT(*) as count
    FROM datasets_metadata
    GROUP BY uploaded_by
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

# Test: Run analytical queries
conn = connect_database()

print("\n Datasets by Uploader:")
df_by_uploader = get_datasets_by_uploader_count(conn)
print(df_by_uploader)

print("\n Large Datasets by Uploader:")
df_large_datasets = get_large_datasets_by_uploader(conn)
print(df_large_datasets)

print("\n Uploaders with Many Datasets (>2):")
df_many_datasets = get_uploaders_with_many_datasets(conn, min_count=2)
print(df_many_datasets)

conn.close()
