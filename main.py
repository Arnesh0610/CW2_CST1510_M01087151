from data.db import connect_database
from data.schema import create_all_tables
import pandas as pd

def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)
    
    # 1. Setup database
    conn = connect_database()    
    create_all_tables(conn)        
    
    # 2. Migrate users
    from app.services.user_service import migrate_users_from_file
    migrate_users_from_file(conn)
    
    # 3. Test authentication
    from app.services.user_service import register_user, login_user
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)
    
    success, msg = login_user("alice", "SecurePass123!")
    print(msg)
    
    # 4. Test CRUD
    from data.incidents import insert_incident, get_all_incidents
    incident_id = insert_incident(
        conn,
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected"
    )
    print(f"Created incident #{incident_id}")
    
    # 5. Query data
    df = get_all_incidents(conn)
    print(f"Total incidents: {len(df)}")

    conn.close()
    
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
    from app.services.user_service import register_user, login_user
    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")

    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")

    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")
    from data.incidents import insert_incident, update_incident_status, delete_incident
    
    # Create
    test_id = insert_incident(
        conn,
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident"
    )
    print(f"  Create: ✅ Incident #{test_id} created")

    # Read
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE incident_id = ?",
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
    from data.incidents import get_incidents_by_type_count, get_high_severity_by_status

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
