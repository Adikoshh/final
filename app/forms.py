from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Jobs

class RegistrationForm(FlaskForm):
   username = StringField('Username', validators=[DataRequired(),Length(min= 4, max=20)])
   first_name = StringField(validators=[DataRequired(),Length(min= 1, max=50)])
   last_name = StringField(validators=[DataRequired(),Length(min= 1, max=50)])
   specialization = StringField(validators=[DataRequired(),Length(min= 1, max=50)])
   email = StringField('Email', validators=[DataRequired(),Email()])
   password = PasswordField('Password', validators=[DataRequired(),Length(min= 4, max=80)])
   confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
   submit = SubmitField('Sign Up') 

   def validate_username(self, username):
      user = User.query.filter_by(username = username.data).first()
      if user:
         raise ValidationError('This username is already taked! Please choose another one.')
         
   def validate_email(self, email):
      email = User.query.filter_by(email = email.data).first()
      if email:
         raise ValidationError('This email is already taked! Please choose another one.')

class LoginForm(FlaskForm):
   email = StringField('Email', validators=[DataRequired(),Email()])
   password = PasswordField('Password', validators=[DataRequired(),Length(min= 4, max=80)])
   remember = BooleanField('Remember me')
   submit = SubmitField('Login') 

class UpdateForm(FlaskForm):
   username = StringField(validators=[DataRequired(),Length(min= 1, max=20)])
   first_name = StringField(validators=[DataRequired(),Length(min= 1, max=50)])
   last_name = StringField(validators=[DataRequired(),Length(min= 1, max=50)])
   phone_number = StringField(validators=[DataRequired(),Length(min= 1, max=50)])
   address = StringField(validators=[DataRequired(),Length(min= 4, max=100)])
   email = StringField(validators=[DataRequired(),Email()])
   submit = SubmitField('Update') 

   def validate_username(self, username):
      if username.data != current_user.username:
         user = User.query.filter_by(username = username.data).first()
         if user:
            raise ValidationError('This username is already taked! Please choose another one.')
         
   def validate_email(self, email):
      if email.data != current_user.email:
         email = User.query.filter_by(email = email.data).first()
         if email:
            raise ValidationError('This email is already taked! Please choose another one.')
