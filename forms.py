from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateField, FileField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    type = SelectField('Type', choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time')], validators=[DataRequired()])
    image = FileField('Image')

class EmployeeApplicationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    nationality = StringField('Nationality', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    work_duration = StringField('Work Duration', validators=[DataRequired()])
    work_location = StringField('Work Location', validators=[DataRequired()])
    work_description = TextAreaField('Work Description', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    year_completed = IntegerField('Year Completed', validators=[DataRequired()])
    # document = FileField('Document')
