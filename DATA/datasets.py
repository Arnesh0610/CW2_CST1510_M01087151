import pandas as pd
from data.db import connect_database

def get_all_datasets(conn):
    #Get all datasets as DataFrame.
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY dataset_id",
        conn
    )
    return df

def insert_dataset(conn, name, rows, columns, uploaded_by, upload_date):

    #Get cursor
    cursor = conn.cursor()

    #Execute and commit
    cursor.execute("""
        INSERT INTO datasets_metadata (name, rows, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?)
    """, (name, rows, columns, uploaded_by, upload_date))
    conn.commit()
    
    # Return cursor.lastrowid
    return cursor.lastrowid


def update_dataset_name(conn, dataset_id, new_name):
    # Write UPDATE SQL: UPDATE datasets_metadata SET name = ? WHERE dataset_id = ?
    cursor = conn.cursor()
    sql = "UPDATE datasets_metadata SET name = ? WHERE dataset_id = ?"

    # Execute and commit
    cursor.execute(sql, (new_name, dataset_id))
    conn.commit()

    # Return cursor.rowcount
    return cursor.rowcount

def delete_dataset(conn, dataset_id):
    # Write DELETE SQL: DELETE FROM datasets_metadata WHERE dataset_id = ?
    cursor = conn.cursor()
    sql = "DELETE FROM datasets_metadata WHERE dataset_id = ?"

    # Execute and commit
    cursor.execute(sql, (dataset_id,))
    conn.commit()

    # Return cursor.rowcount
    return cursor.rowcount

def get_datasets_by_uploader_count(conn):
    query = """
    SELECT uploaded_by, COUNT(*) as count
    FROM datasets_metadata
    GROUP BY uploaded_by
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_large_datasets_by_uploader(conn):
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
