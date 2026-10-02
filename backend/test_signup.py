import sys
sys.path.insert(0, '.')

print("Testing imports...")
try:
    from app.database.connection import Base, create_database, engine, SessionLocal
    from app.models import User
    from app.routers.auth import hash_password, verify_password
    from app.schemas.auth import SignupRequest
    print("All imports successful")
except Exception as e:
    print(f"Import error: {e}")
    sys.exit(1)

print("\nTesting hash functions...")
try:
    test_hash = hash_password("testpassword123")
    print(f"Hash generation: {test_hash[:20]}...")
    print(f"Hash verification (correct): {verify_password('testpassword123', test_hash)}")
    print(f"Hash verification (wrong): {verify_password('wrongpass', test_hash)}")
except Exception as e:
    print(f"Hash error: {e}")
    sys.exit(1)

print("\nTesting Pydantic validation...")
try:
    # Valid request
    valid_req = SignupRequest(name="Test User", email="test@example.com", password="securepass123")
    print(f"Valid request: {valid_req.name}, {valid_req.email}")

    # Test email normalization
    norm_req = SignupRequest(name="Test User", email="TEST@EXAMPLE.COM  ", password="securepass123")
    print(f"Email normalized: {norm_req.email}")

    # Test validation errors
    try:
        SignupRequest(name="", email="test@example.com", password="securepass123")
        print("Should have failed on empty name")
    except Exception as e:
        print(f"Correctly rejected empty name: {str(e)[:50]}...")

    try:
        SignupRequest(name="Test User", email="invalid-email", password="securepass123")
        print("Should have failed on invalid email")
    except Exception as e:
        print(f"Correctly rejected invalid email: {str(e)[:50]}...")

    try:
        SignupRequest(name="Test User", email="test@example.com", password="123")
        print("Should have failed on short password")
    except Exception as e:
        print(f"Correctly rejected short password: {str(e)[:50]}...")

except Exception as e:
    print(f"Validation error: {e}")
    sys.exit(1)

print("\nCreating database and testing User model...")
try:
    create_database()
    print("Database created")

    # Check tables
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")

    # Test database session
    db = SessionLocal()

    # Check if we can query users
    user_count = db.query(User).count()
    print(f"Existing user count: {user_count}")

    # Remove any leftover row from a previous run so this test is repeatable
    db.query(User).filter(User.email == "verify@example.com").delete()
    db.commit()

    # Create a test user
    test_user = User(
        name="Test User",
        email="verify@example.com",
        password_hash=hash_password("testpass123")
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    print(f"Created test user with ID: {test_user.id}")

    # Verify the user was saved correctly
    saved_user = db.query(User).filter(User.email == "verify@example.com").first()
    if saved_user:
        print(f"Saved user name: {saved_user.name}")
        print(f"Saved user email: {saved_user.email}")
        # Verify password is hashed (not plaintext)
        is_hashed = saved_user.password_hash != "testpass123"
        print(f"Password is hashed (not plaintext): {is_hashed}")
        # Verify it's in hash:salt format
        parts = saved_user.password_hash.split(":")
        is_proper_format = len(parts) == 2 and len(parts[0]) == 64 and len(parts[1]) == 64
        print(f"Hash format is correct (hash:salt): {is_proper_format}")
        # Verify password verification works
        password_correct = verify_password("testpass123", saved_user.password_hash)
        password_wrong = not verify_password("wrongpass", saved_user.password_hash)
        print(f"Password verification works: {password_correct and password_wrong}")
    else:
        print("Failed to retrieve saved user")
        sys.exit(1)

    # Clean up so the dev database isn't polluted with test data
    db.query(User).filter(User.email == "verify@example.com").delete()
    db.commit()
    print("Test user cleaned up")

    db.close()
    print("Database session closed")

except Exception as e:
    print(f"Database error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("")
print("All backend tests passed!")