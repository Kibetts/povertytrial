from flask import Flask, request  
from flask_jwt_extended import JWTManager, create_access_token, get_jwt
from flask_restful import Api, Resource

from models import Employee, Employer, Job, Rating, db  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'super-secret'

api = Api(app)
jwt = JWTManager(app)

db.init_app(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
  return user.id

@jwt.user_loader
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
    employee = Employee(
      username=data['username'],
      password=data['password']
    )
    db.session.add(employee)
    db.session.commit()
    return {'message': 'Employee created'}, 201

class EmployerRegister(Resource):

  def post(self):
    data = request.get_json()
    employer = Employer(  
      username=data['username'],
      password=data['password']
    )
    db.session.add(employer)
    db.session.commit()
    return {'message': 'Employer created'}, 201

class EmployeeLogin(Resource):
  
  def post(self):
    data = request.get_json() 
    username = data.get('username')
    password = data.get('password')
    
    employee = Employee.query.filter_by(username=username).first()
    
    if employee and employee.verify_password(password):
      access_token = create_access_token(identity=employee)
      return {'access_token': access_token}
      
    return {'error': 'Invalid credentials'}, 401


class EmployerLogin(Resource):

  def post(self):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password') 

    employer = Employer.query.filter_by(username=username).first()

    if employer and employer.verify_password(password):
      access_token = create_access_token(identity=employer)
      return {'access_token': access_token}
    
    return {'error': 'Invalid credentials'}, 401

api.add_resource(EmployeeRegister, '/employees/register')
api.add_resource(EmployerRegister, '/employers/register')  
api.add_resource(EmployeeLogin, '/employees/login')
api.add_resource(EmployerLogin, '/employers/login')

class EmployeeResource(Resource):
  
  def get(self):
    employees = Employee.query.all()
    return {'employees': [e.to_dict() for e in employees]}

api.add_resource(EmployeeResource, '/employees')

class EmployerResource(Resource):

  def get(self):
    employers = Employer.query.all()
    return {'employers': [e.to_dict() for e in employers]}
  
api.add_resource(EmployerResource, '/employers')

class JobResource(Resource):

  def get(self):
    jobs = Job.query.all()
    return {'jobs': [j.to_dict() for j in jobs]}

  @role_required('employer')
  def post(self):
    data = request.get_json()
    job = Job(
      title=data['title'], 
      description=data['description']
    )
    db.session.add(job)
    db.session.commit()
    return job.to_dict(), 201

api.add_resource(JobResource, '/jobs')

class RatingResource(Resource):

  def get(self):
    ratings = Rating.query.all()
    return {'ratings': [r.to_dict() for r in ratings]}

  def post(self):
    data = request.get_json()
    rating = Rating(
      stars=data['stars'],
      comment=data['comment']  
    )
    db.session.add(rating)
    db.session.commit()
    return rating.to_dict(), 201

api.add_resource(RatingResource, '/ratings')

if __name__ == '__main__':
  app.run()