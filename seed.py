
from app import app, db
import random
from faker import Faker
from models import Employee, Employer, Job, Rating, EmployeeApplication, CompanyProfile

fake = Faker()

with app.app_context():
    for i in range(10):
        employee = Employee(
            name=fake.name(),
            email=fake.email(),
            username=fake.user_name(),
            password=fake.password(),
            skills=fake.text(),
            experience=random.randint(1, 10)
        )
        db.session.add(employee)

    for i in range(10):
        job = Job(
            title=fake.job(),
            description=fake.sentence(),
            location=fake.city(),
            type='Full-time',
            salary=random.randint(30000, 100000),
            image=fake.image()
        )
        db.session.add(job)

    db.session.commit()

    for i in range(5):
        employer = Employer(
            name=fake.company(),
            username=fake.user_name(),
            email=fake.email(),
            description=fake.catch_phrase(),
            password=fake.password()
        )
        db.session.add(employer)

    for i in range(5):
        employer = random.choice(Employer.query.all())
        employee = random.choice(Employee.query.all())
        employee_application = EmployeeApplication(
            job=random.choice(Job.query.all()),
            employee=employee,
            name=fake.name(),
            date_of_birth=fake.date_of_birth(),
            nationality=fake.country(),
            city=fake.city(),
            email=fake.email(),
            mobile=fake.phone_number(),
            role=fake.job(),
            work_duration=fake.word(),
            work_location=fake.city(),
            work_description=fake.sentence(),
            school=fake.company(),
            major=fake.word(),
            year_completed=fake.random_int(min=1990, max=2022)
        )
        db.session.add(employee_application)

    for employer in Employer.query.all():
        company_profile = CompanyProfile(
            employer=employer,
            business_industry=fake.bs(),
            employee_size=fake.random_element(elements=('Small', 'Medium', 'Large')),
            base_currency=fake.currency_code(),
            continent=fake.random_element(elements=('Asia', 'Europe', 'North America', 'South America', 'Africa')),
            country=fake.country(),
            city=fake.city(),
            address=fake.address(),
            primary_contact_email=fake.email(),
            primary_contact_phone=fake.phone_number()
        )
        db.session.add(company_profile)

    for i in range(20):
        employee = random.choice(Employee.query.all())
        employer = random.choice(Employer.query.all())
        rating = Rating(
            rating=random.randint(1, 5),
            date=fake.date_time(),
            employee=employee,
            employer=employer
        )
        db.session.add(rating)

    db.session.commit()




################################################   more realistic data   #######################################


# import json
# from app import app, db
# from models import Employee, Employer, Job, Rating, EmployeeApplication, CompanyProfile
# from datetime import datetime

# # Create JSON data for employees
# employees = [
#     {
#         "name": "John Doe",
#         "email": "johndoe@example.com",
#         "username": "johndoe123",
#         "password": "securepassword",
#         "skills": "Python, JavaScript, SQL",
#         "experience": 5
#     },
#     # Add more employee data
# ]

# # Create JSON data for jobs
# jobs = [
#     {
#         "title": "Software Engineer",
#         "description": "We are looking for a software engineer with strong programming skills.",
#         "location": "New York",
#         "type": "Full-time",
#         "salary": 80000,
#         "image": "job_image_url"
#     },
#     # Add more job data
# ]

# # Create JSON data for employers
# employers = [
#     {
#         "name": "Acme Inc.",
#         "username": "acmeinc",
#         "email": "contact@acme.com",
#         "description": "Leading technology company",
#         "password": "securepassword"
#     },
#     # Add more employer data
# ]

# # Create JSON data for employee applications
# employee_applications = [
#     {
#         "job_id": 1,  # Referencing the job with ID 1
#         "employee_id": 1,  # Referencing the employee with ID 1
#         "name": "John Doe",
#         "date_of_birth": "1990-01-15",
#         "nationality": "USA",
#         "city": "New York",
#         "email": "john.doe@example.com",
#         "mobile": "+1 (123) 456-7890",
#         "role": "Software Engineer",
#         "work_duration": "5 years",
#         "work_location": "New York",
#         "work_description": "Worked on web development projects.",
#         "school": "University of XYZ",
#         "major": "Computer Science",
#         "year_completed": 2015
#     },
#     # Add more employee application data
# ]

# # Create JSON data for company profiles
# company_profiles = [
#     {
#         "employer_id": employers.index(employer) + 1,
#         "business_industry": "Technology",
#         "employee_size": "Large",
#         "base_currency": "USD",
#         "continent": "North America",
#         "country": "USA",
#         "city": "New York",
#         "address": "123 Main St, Suite 456",
#         "primary_contact_email": "contact@acme.com",
#         "primary_contact_phone": "+1 (123) 456-7890"
#     },
#     # Add more company profile data
# ]

# # Create JSON data for ratings
# ratings = [
#     {
#         "rating": 4,
#         "date": "2023-01-15T10:30:00",
#         "employee_id": 1,  # Referencing the employee with ID 1
#         "employer_id": 1  # Referencing the employer with ID 1
#     },
#     # Add more rating data
# ]

# # Create a dictionary to store all JSON data
# data = {
#     "employees": employees,
#     "jobs": jobs,
#     "employers": employers,
#     "employee_applications": employee_applications,
#     "company_profiles": company_profiles,
#     "ratings": ratings
# }

# with app.app_context():
#     for employee_data in data['employees']:
#         employee = Employee(
#             name=employee_data["name"],
#             email=employee_data["email"],
#             username=employee_data["username"],
#             password=employee_data["password"],
#             skills=employee_data["skills"],
#             experience=employee_data["experience"]
#         )
#         db.session.add(employee)

#     for job_data in data['jobs']:
#         job = Job(
#             title=job_data["title"],
#             description=job_data["description"],
#             location=job_data["location"],
#             type=job_data["type"],
#             salary=job_data["salary"],
#             image=job_data["image"]
#         )
#         db.session.add(job)

#     for employer_data in data['employers']:
#         employer = Employer(
#             name=employer_data["name"],
#             username=employer_data["username"],
#             email=employer_data["email"],
#             description=employer_data["description"],
#             password=employer_data["password"]
#         )
#         db.session.add(employer)

#     for app_data in data['employee_applications']:
#         app = EmployeeApplication(
#             job_id=app_data["job_id"],
#             employee_id=app_data["employee_id"],
#             name=app_data["name"],
#             date_of_birth=app_data["date_of_birth"],
#             nationality=app_data["nationality"],
#             city=app_data["city"],
#             email=app_data["email"],
#             mobile=app_data["mobile"],
#             role=app_data["role"],
#             work_duration=app_data["work_duration"],
#             work_location=app_data["work_location"],
#             work_description=app_data["work_description"],
#             school=app_data["school"],
#             major=app_data["major"],
#             year_completed=app_data["year_completed"]
#         )
#         db.session.add(app)

#     for profile_data in data['company_profiles']:
#         employer = Employer.query.get(profile_data["employer_id"])
#         company_profile = CompanyProfile(
#             employer=employer,
#             business_industry=profile_data["business_industry"],
#             employee_size=profile_data["employee_size"],
#             base_currency=profile_data["base_currency"],
#             continent=profile_data["continent"],
#             country=profile_data["country"],
#             city=profile_data["city"],
#             address=profile_data["address"],
#             primary_contact_email=profile_data["primary_contact_email"],
#             primary_contact_phone=profile_data["primary_contact_phone"]
#         )
#         db.session.add(company_profile)

#     for rating_data in data['ratings']:
#         employee = Employee.query.get(rating_data["employee_id"])
#         employer = Employer.query.get(rating_data["employer_id"])
#         rating = Rating(
#             rating=rating_data["rating"],
#             date=rating_data["date"],
#             employee=employee,
#             employer=employer
#         )
#         db.session.add(rating)

#     db.session.commit()
