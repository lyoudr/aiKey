from src.models.database import get_db
from src.models.role import Role
from src.models.organization import Organization
from src.repositories import user_repository
from src.utils.authenticate import get_password_hash

def seed_users():
    db = next(get_db())

    # Fetch roles and organizations
    roles = {role.name: role.id for role in db.query(Role).all()}
    organizations = {org.name: org.id for org in db.query(Organization).all()}

    # Define a default password and hash it 
    default_pass = "SecureP@ssw0rd"
    hashed_pass = get_password_hash(default_pass)

    # Sample users
    users = [
        {
            "name": "Admin",
            "email": "aiphas@example.com",
            "user_type": "AIPHAS",
            "role_id": roles.get("Admin"),
            "organization_id": None,
            "hashed_password": hashed_pass
        },
        {
            "name": "Dr. Bob",
            "email": "bob.doctor@example.com",
            "user_type": "DOCTOR",
            "role_id": roles.get("Doctor"),
            "organization_id": organizations.get("Cardiology"),
            "hashed_password": hashed_pass
        },
        {
            "name": "Dr. Nancy",
            "email": "nancy.doctor@example.com",
            "user_type": "DOCTOR",
            "role_id": roles.get("Doctor"),
            "organization_id": organizations.get("Neurology"),
            "hashed_password": hashed_pass
        },
        {
            "name": "Dr. Tom",
            "email": "tom.doctor@example.com",
            "user_type": "DOCTOR",
            "role_id": roles.get("Doctor"),
            "organization_id": organizations.get("Oncology"),
            "hashed_password": hashed_pass
        }
    ]

    # Insert users
    user_repository.batch_insert_users(users)

    print("Users seeded successfully.")