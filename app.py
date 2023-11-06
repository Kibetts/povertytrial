import os
from forms import JobForm, EmployeeApplicationForm
from flask import Flask, request, make_response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, verify_jwt_in_request
from flask_restful import Api, Resource, reqparse
from datetime import datetime
from flask_cors import CORS


# from flask_uploads import UploadSet, configure_uploads, IMAGES
# from flask_wtf.csrf import CSRFProtect
# from werkzeug.utils import secure_filename

from models import *
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get("DATABASE_URL")
app.config['JWT_SECRET_KEY'] = 'Tingatales1'
app.config['SECRET_KEY'] = 'Tingatales1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#postgres://skillhunter:AAl15UpE0pn5nZYm0X1ZcvrBfGIdhy88@dpg-cl4gmfpnovjs739jgpgg-a.oregon-postgres.render.com/skillhunter_hkko

CORS(app)
# uploaded_documents = UploadSet('documents', extensions=('pdf', 'doc', 'docx', 'txt'))
# app.config['UPLOADED_DOCUMENTS_DEST'] = 'path_to_upload_folder'  # to replace with the actual folder path on render
# app.config['UPLOADED_DOCUMENTS_URL'] = 'url_to_upload_folder' # to replace with the actual folder path on render
# configure_uploads(app, uploaded_documents)

def get_access_token():
    auth_header = request.headers.get("Authorization")
    print("Authorization Header:", auth_header)   ##check if auth header is retrieved

    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]
    else:
        return None


api = Api(app)
db.init_app(app)
from flask_migrate import Migrate
migrate = Migrate(app, db)

jwt = JWTManager(app)

           ##############Define a function to get the current user based on the access token#########################
def get_current_user(access_token):
    try:
        user_identity = get_jwt()
        if user_identity:
            if user_identity['role'] == 'employee':
                return find_employee(user_identity['id'])
            elif user_identity['role'] == 'employer':
                return find_employer(user_identity['id'])
    except Exception as e:
        pass
    return None

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def add_claims_to_jwt(identity):
    if isinstance(identity, Employee):
        return {'role': 'employee'}
    elif isinstance(identity, Employer):
        return {'role': 'employer'}




def role_required(role):
    def wrapper(fn):
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims['role'] != role:
                return {'message': 'Unauthorized'}, 401
            return fn(*args, **kwargs)

        return decorator

    return wrapper

class EmployeeRegister(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')

        if not email or not username or not password or not name:
            return {'error': 'Name, email, username, and password are required fields'}, 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        employee = Employee(
            name=name,
            email=email,
            username=username,
            password=hashed_password.decode('utf-8')
        )

        db.session.add(employee)
        db.session.commit()
        return {'message': 'Employee created'}, 201


class EmployerRegister(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')

        if not email or not username or not password or not name:
            return {'error': 'Name, email, username, and password are required fields for employer registration'}, 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        employer = Employer(
            name=name,
            email=email,
            username=username,
            password=hashed_password.decode('utf-8')
        )

        db.session.add(employer)
        db.session.commit()
        return {'message': 'Employer created'}, 201



class EmployeeLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not (email or username):
            return {'error': 'Either email or username is required for login'}, 400

        employee = find_employee(email, username)

        if employee and bcrypt.checkpw(password.encode('utf-8'), employee.password.encode('utf-8')):
            access_token = create_access_token(identity=employee)
            return {'access_token': access_token}

        return {'error': 'Invalid credentials'}, 401

class EmployerLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not (email or username):
            return {'error': 'Either email or username is required for login'}, 400

        employer = find_employer(email, username)

        if employer and bcrypt.checkpw(password.encode('utf-8'), employer.password.encode('utf-8')):
            access_token = create_access_token(identity=employer)
            return {'access_token': access_token}

        return {'error': 'Invalid credentials'}, 401


def find_employee(email, username):
    if email:
        return Employee.query.filter_by(email=email).first()
    elif username:
        return Employee.query.filter_by(username=username).first()
    return None


def find_employer(email, username):
    if email:
        return Employer.query.filter_by(email=email).first()
    elif username:
        return Employer.query.filter_by(username=username).first()
    return None
api.add_resource(EmployeeRegister, '/employees/register')
api.add_resource(EmployerRegister, '/employers/register')
api.add_resource(EmployeeLogin, '/employees/login')
api.add_resource(EmployerLogin, '/employers/login')

              ######################Resource for employers to post jobs##########################
class JobPostResource(Resource):
    @jwt_required()
    def post(self):
        form = JobForm()
        parser = reqparse.RequestParser()
        parser.add_argument('access_token', type=str, location='headers')  # You may need to adjust this header
        args = parser.parse_args()

        # print("Access Token:", args['access_token'])  # check if access token is returned

        if not args['access_token']:
            return {'error': 'Access token is required'}, 400

        current_user = get_current_user(args['access_token'])
        print("current user", current_user)
        if not current_user:
            return {'error': 'Invalid access token'}, 401

        if current_user['role'] != 'employer':
            return {'error': 'Only employers can post jobs'}, 403

        if form.validate():
                 ##################Process form data and save the job to the database########################
            new_job = Job(
                title=form.title.data,
                description=form.description.data,
                salary=form.salary.data,
                location=form.location.data,
                type=form.type.data,
                image=form.image.data.read() if form.image.data else None
            )
            db.session.add(new_job)
            db.session.commit()
            return {'message': 'Job posted successfully'}, 201
        return {'error': form.errors}, 400

           ###########Resource for employees to apply for a job################
class EmployeeApplicationResource(Resource):
    def post(self, job_id):
        form = EmployeeApplicationForm()

        if not form.validate_on_submit():
            return {'error': form.errors}, 400

        parser = reqparse.RequestParser()
        parser.add_argument('access_token', type=str, location='headers')
        args = parser.parse_args()

        if not args['access_token']:
            return {'error': 'Access token is required'}, 400

        current_user = get_current_user(args['access_token'])

        if not current_user:
            return {'error': 'Invalid access token'}, 401

        if current_user['role'] != 'employee':
            return {'error': 'Only employees can apply for jobs'}, 403

        job = Job.query.get(job_id)
        if not job:
            return {'error': 'Job not found'}, 404

        try:
            new_application = EmployeeApplication(
                job=job,
                employee=current_user,
                name=form.name.data,
                date_of_birth=form.date_of_birth.data,
                nationality=form.nationality.data,
                city=form.city.data,
                email=form.email.data,
                mobile=form.mobile.data,
                role=form.role.data,
                work_duration=form.work_duration.data,
                work_location=form.work_location.data,
                work_description=form.work_description.data,
                school=form.school.data,
                major=form.major.data,
                year_completed=form.year_completed.data
            )

            db.session.add(new_application)
            db.session.commit()

            return {'message': 'Application submitted successfully'}, 201

        except Exception as e:
            return {'error': 'Error submitting the application'}, 500



api.add_resource(JobPostResource, '/employers/post_job')
api.add_resource(EmployeeApplicationResource, '/employees/apply/<int:job_id>')

class Home(Resource):
    def get(self):
        return 'Welcome to SkillHunter'

api.add_resource(Home, '/')

class EmployeeResource(Resource):

  def get(self):
    employees = Employee.query.all()
    return {'employees': [emp.to_dict() for emp in employees]}
  
  def post(self):
    data = request.get_json() 
    new_employee = Employee(**data)
    db.session.add(new_employee)
    db.session.commit()
    return new_employee.to_dict(), 201

api.add_resource(EmployeeResource, '/employees')

class EmployeeById(Resource):

    def get(self, employee_id):
        employee = Employee.query.get(employee_id)
        if employee:
            return employee.to_dict()
        return {'error': 'Employee not found'}, 404

    def patch(self, employee_id):
        employee = Employee.query.get(employee_id)
        if employee:
            for key, value in request.get_json().items():
                setattr(employee, key, value)
            db.session.commit()
            return employee.to_dict()
        return {'error': 'Employee not found'}, 404

api.add_resource(EmployeeById, '/employees/<int:employee_id>')

class EmployerResource(Resource):

    def get(self):
        employers = Employer.query.all()
        return {'employers': [e.to_dict() for e in employers]}

    def post(self):
        data = request.get_json()
        new_employer = Employer(**data)
        db.session.add(new_employer)
        db.session.commit()
        return new_employer.to_dict(), 201

api.add_resource(EmployerResource, '/employers')

class EmployerById(Resource):

    def get(self, employer_id):
        employer = Employer.query.get(employer_id)
        if employer:
            return employer.to_dict()
        return {'error': 'Employer not found'}, 404

    def patch(self, employer_id):
        employer = Employer.query.get(employer_id)
        if employer:
            for key, value in request.get_json().items():
                setattr(employer, key, value)
            db.session.commit()
            return employer.to_dict()
        return {'error': 'Employer not found'}, 404

api.add_resource(EmployerById, '/employers/<int:employer_id>')

class JobResource(Resource):

    def get(self):
        jobs = Job.query.all()
        return {'jobs': [j.to_dict() for j in jobs]}

    @role_required('employer')
    def post(self):
        data = request.get_json()
        new_job = Job(**data)
        db.session.add(new_job)
        db.session.commit()
        return new_job.to_dict(), 201

api.add_resource(JobResource, '/jobs')

class JobById(Resource):

    def get(self, job_id):
        job = Job.query.get(job_id)
        if job:
            return job.to_dict()
        return {'error': 'Job not found'}, 404

    @role_required('employer')
    def patch(self, job_id):
        job = Job.query.get(job_id)
        if job:
            return job.to_dict()
        return {'error': 'Job not found'}, 404

    @role_required('employer')
    def delete(self, job_id):
        job = Job.query.get(job_id)
        if job:
            db.session.delete(job)
            db.session.commit()
            return {'deleted': True}
        return {'error': 'Job not found'}, 404

api.add_resource(JobById, '/jobs/<int:job_id>')

class RatingResource(Resource):

    def get(self):
        ratings = Rating.query.all()
        return {'ratings': [r.to_dict() for r in ratings]}

    def post(self):
        data = request.get_json()
        data['date'] = datetime.now()
        new_rating = Rating(**data)
        db.session.add(new_rating)
        db.session.commit()
        return new_rating.to_dict(), 201

api.add_resource(RatingResource, '/ratings')

class RatingByID(Resource):
    def get(self, id):
        rating = Rating.query.get(int(id))
        response_dict = rating.to_dict()
        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response

    def patch(self, id):
        rating = Rating.query.get(int(id))
        for attr in request.json:
            setattr(rating, attr, request.json[attr])
        db.session.add(rating)
        db.session.commit()

        response_dict = rating.to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response

    def delete(self, id):
        rating = Rating.query.get(int(id))
        db.session.delete(rating)
        db.session.commit()

        response_dict = {
            'message': 'rating succesfully deleted'
        }

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

api.add_resource(RatingByID, '/ratings/<int:id>')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()


####postgresql://brayan:2vGSUcIdedE8SSyINO6cJhlz31APGbCE@dpg-cl37ci0t3kic73d8e7ag-a.oregon-postgres.render.com/skillhunter