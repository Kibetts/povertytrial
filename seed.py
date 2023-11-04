
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
