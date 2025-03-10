from src.repositories import role_repository
from src.models.database import get_db
from src.models.role import Role, Permission


def seed_roles_and_permissions():
    db = next(get_db())

    # Sample roles
    roles = [
        {"name": "ADMIN"},
        {"name": "DOCTOR"}
    ]
    
    # Sample permissions
    permissions = [
        {"name": "read_patient_records"},
        {"name": "write_patient_records"},
        {"name": "manage_users"}
    ]

    # Insert roles and permissions
    role_repository.batch_insert_roles(roles)
    role_repository.batch_insert_permissions(permissions)

    # Fetch inserted roles and permissions
    inserted_roles = db.query(Role).all()
    inserted_permissions = db.query(Permission).all()

    # Assign permissions to roles (example mapping)
    role_permissions_mapping = {
        "Admin": ["manage_users", "read_patient_records", "write_patient_records"],
        "Doctor": ["read_patient_records", "write_patient_records"]
    }

    for role in inserted_roles:
        role.permissions = [
            perm for perm in inserted_permissions if perm.name in role_permissions_mapping.get(role.name, [])
        ]

    db.commit()
    print("Roles and permissions seeded successfully.")
