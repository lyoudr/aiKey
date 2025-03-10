from src.seeders import (
    medical_seeder,
    organization_seeder,
    patient_seeder,
    role_seeder,
    user_seeder
)

def seed_data():
    organization_seeder.seed()
    patient_seeder.seed()
    medical_seeder.seed()
    role_seeder.seed_roles_and_permissions()
    user_seeder.seed_users()


if __name__ == "__main__":
    seed_data()
