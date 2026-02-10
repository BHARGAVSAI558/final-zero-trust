"""
Migration script to hash existing plaintext passwords in the database.
Run this ONCE after upgrading to the new authentication system.
"""

from database import get_db
from security import hash_password

def migrate_passwords():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Get all users with plaintext passwords
    cursor.execute("SELECT id, username, password FROM users")
    users = cursor.fetchall()
    
    print(f"Found {len(users)} users to migrate...")
    
    for user in users:
        # Check if password is already hashed (bcrypt hashes start with $2b$)
        if user['password'].startswith('$2b$'):
            print(f"✓ {user['username']} - Already hashed, skipping")
            continue
        
        # Hash the plaintext password
        hashed = hash_password(user['password'])
        
        # Update in database
        cursor.execute(
            "UPDATE users SET password=%s WHERE id=%s",
            (hashed, user['id'])
        )
        print(f"✓ {user['username']} - Password hashed successfully")
    
    db.commit()
    print("\n✅ Migration completed!")
    print("⚠️  Make sure to update your login credentials if needed.")

if __name__ == "__main__":
    print("=" * 50)
    print("PASSWORD MIGRATION SCRIPT")
    print("=" * 50)
    print("\nThis will hash all plaintext passwords in the database.")
    confirm = input("Continue? (yes/no): ")
    
    if confirm.lower() == 'yes':
        migrate_passwords()
    else:
        print("Migration cancelled.")
