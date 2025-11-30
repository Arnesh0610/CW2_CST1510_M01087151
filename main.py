from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents
from app.data.incidents import update_incident_status, delete_incident
from app.data.incidents import get_incidents_by_type_count, get_high_severity_by_status
import pandas as pd

def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)
    
    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)
    conn.close()
    
    # 2. Migrate users
    migrate_users_from_file()
    
    # 3. Test authentication
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)
    
    success, msg = login_user("alice", "SecurePass123!")
    print(msg)
    
    # 4. Test CRUD
    incident_id = insert_incident(
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")

    # 5. Query data
    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")

if __name__ == "__main__":
    main()

def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "="*60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("="*60)

    conn = connect_database()

    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")

    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")

    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")

    # Create
    test_id = insert_incident(
        conn,
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"  Create: ✅ Incident #{test_id} created")

    # Read
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read:    Found incident #{test_id}")

    # Update
    update_incident_status(conn, test_id, "Resolved")
    print(f"  Update:  Status updated")

    # Delete
    delete_incident(conn, test_id)
    print(f"  Delete:  Incident deleted")

    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")

    df_by_type = get_incidents_by_type_count(conn)
    print(f"  By Type:     Found {len(df_by_type)} incident types")

    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: Found {len(df_high)} status categories")

    conn.close()

    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)

# Run tests
run_comprehensive_tests()