from flask import flash, redirect, render_template, url_for, request
from app.forms import LoginForm, RegistrationForm, UpdateForm
from app.models import User, Jobs
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
# import json
# import requests

# url = "https://linkedin-jobs-search.p.rapidapi.com/"

# payload = {
# 	"search_terms": "python programmer",
# 	"location": "30301",
# 	"page": "1"
# }
# headers = {
# 	"content-type": "application/json",
# 	"X-RapidAPI-Key": "f8452952dcmsh2100f597a8ea06cp12c3cbjsn7d06c664e39d",
# 	"X-RapidAPI-Host": "linkedin-jobs-search.p.rapidapi.com"
# }

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/about')
def about():
   return render_template('about.html', title='About')

@app.route('/sign-in',  methods=['POST', 'GET'])
def sign_in():
   if current_user.is_authenticated:
      return redirect(url_for('home'))
   form = LoginForm()
   if form.validate_on_submit():
      user = User.query.filter_by(email = form.email.data).first()
      if user and bcrypt.check_password_hash(user.password, form.password.data):
         login_user(user, remember=form.remember.data)
         next_page = request.args.get('next')
         return redirect(next_page) if next_page else redirect(url_for('home'))
      else:
         flash('Login unsuccessful! Please check the email and password!', 'danger')
   return render_template('sign-in.html', title='Sign-in', form=form)

@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
   if current_user.is_authenticated:
      return redirect(url_for('home'))
   form = RegistrationForm()
   if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      user = User(username = form.username.data, 
                           first_name = form.first_name.data, 
                           last_name = form.last_name.data, 
                           specialization = form.specialization.data, 
                           email = form.email.data, 
                           password = hashed_password)
      db.session.add(user)
      db.session.commit()
      flash(f'Your account has been created! You are now able to log in!', 'success')
      return redirect(url_for('sign_in'))
   
   return render_template('sign-up.html', title='Sign-up', form=form)

@app.route("/logout")
def logout():
   logout_user()
   return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
   image_file = url_for('static', filename='img/' + current_user.image_file)
   return render_template('account.html', title = 'Account', image_file = image_file)

@app.route("/account-update", methods=['POST', 'GET'])
@login_required
def account_update():
   form = UpdateForm()
   image_file = url_for('static', filename='img/' + current_user.image_file)
   if request.method == "GET":
      form.username.data = current_user.username
      form.first_name.data = current_user.first_name
      form.last_name.data = current_user.last_name
      form.phone_number.data = current_user.phone_number
      form.address.data = current_user.address
      form.email.data = current_user.email
      return render_template('account-update.html', title = 'Account', image_file = image_file, form = form)
   elif request.method == "POST":
      if form.validate_on_submit:
         current_user.username = form.username.data
         current_user.first_name = form.first_name.data
         current_user.last_name = form.last_name.data
         current_user.phone_number = form.phone_number.data
         current_user.address = form.address.data
         current_user.email = form.email.data
         db.session.commit()  
         flash("Your account has been updated!", 'success')
         return redirect(url_for('account'))
      
@app.route('/resume')
@login_required
def resume():
   users = User.query.all()
   image_file = url_for('static', filename='img/' + current_user.image_file)
   return render_template('resume.html', users = users, image_file = image_file)

@app.route('/jobs')
def jobs():  
   # response = requests.request("POST", url, json=payload, headers=headers)
   # response = response.json() 
   # for res in response:
   #    job = Jobs(job_title = res['job_title'], 
   #                      company_name = res['company_name'], 
   #                      posted_date = res['posted_date'], 
   #                      job_location = res['job_location'], 
   #                      job_url = res['job_url'])
   #    db.session.add(job)
   #    db.session.commit()
   jobs = Jobs.query.all()
   return render_template('jobs.html', jobs = jobs)


@app.route('/user_page/<user_id>', methods = ['GET', 'POST'])
@login_required
def user_page(user_id):
    current_user = db.session.query(User).filter(User.id==user_id).first()
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template("user_page.html", user=current_user, image_file = image_file)