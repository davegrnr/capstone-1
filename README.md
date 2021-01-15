<<<<<<< HEAD
# Capstone-1

# Project Objective:
1. ### Actors Involved:  
 - User (Job Searcher)
 -  Job Creater (Admin posting jobs to API) 

2. ### Auth Module:
 -  Login Page - log in with email/password JWT token using bcrypt
3. ###  Home page:  
 - Logged in users see a list of their favorited jobs and search form to get new jobs list.  
 Anonymouse users see a list of jobs and sign up routes. If they try to click a job or favorite, they will be redirected to the sign up page.  
4. ###  Features:  
 -  The user will have a select field where they can choose an industry from a list and receive a new page of available jobs once submitted. They can then favorite jobs to save them for later use *Further study: implement some more advanced sorting/filtering beyond industry*
5. ### User Profile Page:
 - Logged in user can see a list of their favorited jobs as well as go to an edit page where the user can edit bio/location/email etc... *Maybe implement a feature that lets the user choose a default job type? E.g. a logged in software engineer will, by default, only see software engineering jobs*


# Technical details
1. ### Frontend:  
 - HTML, JS, CSS as Jinja template

2. ### Backend:
 -  Python via Flask
 
3. ###  Database:  
 - PostgreSQL
 
4. ###  Hosting:  
 -  Heroku
