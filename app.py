import os

from bs4 import BeautifulSoup
from flask import Flask, render_template, request, flash, redirect, session, g, json, jsonify
from flask_cors import CORS, cross_origin
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests

from models import db, connect_db, User, SavedJob
from forms import UserAddForm, LoginForm , EditUserForm, SearchJobsForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///job_locker'))

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "so secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
cors = CORS(app)
soup = BeautifulSoup()



##############################################################
# Homepage


@app.route('/')
def homepage():
    """Shows homepage:

    not-logged-in: prompt for signup
    logged in: display saved jobs
    """

    # if g.user:
    #     job_ids = [j.id for j in g.user.]

    return render_template('home.html')

###############################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handles a user signup.

    Create new user > add to DB > Redirect to home

    Check form validity/present if not valid

    If username taken, flash msg and re-present form
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash(f"You are now logged out!", "success")
    return redirect('/')

################################################################
#Search Route, Save Job Route

@app.route('/search/<int:user_id>', methods=["GET", "POST"])
def search_jobs(user_id):
    user = User.query.get_or_404(user_id)
    json_data = {}

    if not g.user:
        flash("Please login or sign up first.")
        return redirect('/signup')

    user = g.user
    form = SearchJobsForm()
   
    if form.validate_on_submit():
         # Check for all fields filled out
        if form.data['search_term'] and form.data['category'] and form.data['company_name']:
            search = form.data['search_term'].strip()
            category = form.data['category']
            company_name = form.data['company_name'].strip()
            json_data = requests.get(f"https://remotive.io/api/remote-jobs?category={category}&search={search}&company_name={company_name}limit=25").json()
            

            return render_template('/search.html', form=form, json_data=json_data)

        # Check if only 'search_term' and 'category'
        elif form.data['search_term'] and form.data['category']:
            search = form.data['search_term'].strip()
            category = form.data['category']
            json_data = requests.get(f"https://remotive.io/api/remote-jobs?category={category}&search={search}&limit=25").json()

            return render_template('/search.html', form=form, json_data=json_data)

        # Check if only 'company_name' and 'category'
        elif form.data['company_name'] and form.data['category']:
            company_name= form.data['company_name'].strip()
            category = form.data['category']
            json_data = requests.get(f"https://remotive.io/api/remote-jobs?category={category}&company_name={company_name}&limit=25").json()

            return render_template('/search.html', form=form, json_data=json_data)

        # Check if only 'category'
        elif form.data['category']:
                category = form.data['category']
                json_data = requests.get(f"https://remotive.io/api/remote-jobs?category={category}&limit=25").json()

                return render_template('/search.html', form=form, json_data=json_data)

        # Else return all jobs
        else:
                json_data = requests.get(f"https://remotive.io/api/remote-jobs?limit=25").json()

                return render_template('/search.html', form=form, json_data=json_data)

    return render_template('/search.html', form=form, json_data=json_data)
        

@app.route('/api/saved-jobs', methods=["POST"])
@cross_origin()
def list_saved_jobs():
    new_saved_job = SavedJob(id=request.json["saved_job_id"], user_id=request.json["user_id"])
    db.session.add(new_saved_job)
    db.session.commit()
    response_json = jsonify(job=new_saved_job.serialize())
    return (response_json, 201)
    

    # data = request.get_json()
    # return request.data

    # new_saved_job = SavedJob(id=data["saved_job_id"],user_id=data["user_id"])
    # response_json = jsonify(job=new_saved_job.serialize())
    # return (response_json, 201)

    



################################################################
#User routes

@app.route('/users/<int:user_id>')
def show_user_page(user_id):
    """Display user profile"""

    user=User.query.get_or_404(user_id)

    
    return render_template('/users/show.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """Edit user profile. If Unauthorized, redirect"""

    if not g.user:
        flash("Access denied.", "danger")

    user = g.user
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.location = form.location.data
            user.bio = form.bio.data

            db.session.commit()
            return redirect(f"/users/{user.id}")

        flash("Invalid password, please try again", 'danger')

    return render_template('/users/edit.html', form=form, user_id=user.id, user=user)

@app.route('/users/<int:user_id>/saved-jobs')
def show_saved_jobs(user_id):

    saved_jobs = SavedJob.query.filter(SavedJob.user_id == user_id).all()

    return render_template('/users/saved-jobs.html', saved_jobs=saved_jobs)