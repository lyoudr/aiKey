from datetime import date

from src.repositories import patient_repository

def seed():
    # Sample data for the patients
    data = [
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': date(1985, 7, 15),  # Example DOB
            'gender': 'MALE',
            'contact_number': '123-456-7890',
            'address': '123 Main St, Springfield',
            'email': 'john.doe@example.com'
        },
        {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'date_of_birth': date(1990, 4, 22),  # Example DOB
            'gender': 'FEMALE',
            'contact_number': '987-654-3210',
            'address': '456 Oak Rd, Springfield',
            'email': 'jane.smith@example.com'
        },
        {
            'first_name': 'Sam',
            'last_name': 'Johnson',
            'date_of_birth': date(1978, 9, 10),  # Example DOB
            'gender': 'MALE',
            'contact_number': '555-123-4567',
            'address': '789 Pine Ave, Springfield',
            'email': 'sam.johnson@example.com'
        },
        {
            'first_name': 'Emily',
            'last_name': 'Davis',
            'date_of_birth': date(2000, 12, 5),  # Example DOB
            'gender': 'FEMALE',
            'contact_number': '321-654-9870',
            'address': '101 Birch Blvd, Springfield',
            'email': 'emily.davis@example.com'
        }
    ]

    # Call the batch insert function to add the sample data to the database
    patient_repository.batch_insert(data)