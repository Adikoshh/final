from datetime import datetime
from app import app, db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key = True)
   username = db.Column(db.String(50), nullable = False, unique = True)
   first_name = db.Column(db.String(50), nullable = True)
   last_name = db.Column(db.String(50), nullable = True)
   specialization = db.Column(db.String(50), nullable = True)
   phone_number = db.Column(db.String(50), nullable = True)
   address = db.Column(db.String(100), nullable = True)
   email = db.Column(db.String(120), nullable = False, unique = True)
   image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
   password = db.Column(db.String(80), nullable = False)

   def __repr__(self):
      return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Jobs(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   job_title = db.Column(db.String(30), nullable = False)
   company_name = db.Column(db.String(120), nullable = False)  
   posted_date = db.Column(db.String(50), nullable = False)
   job_location = db.Column(db.String(120), nullable = False)
   job_url = db.Column(db.String(50), nullable = False, unique = True)

   def __repr__(self):
      return f"Jobs('{self.job_title}', '{self.company_name}', '{self.posted_date}', '{self.job_location}', '{self.job_url}')"
      
with app.app_context():
    db.create_all()
