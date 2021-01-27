from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length

# listttt =  {"id": 19, "name": "Software Development", "slug": "software-dev"}, {"id": 18, "name": "Customer Service", "slug": "customer-support"}, {"id": 21, "name": "Design", "slug": "design"}, {"id": 28, "name": "Marketing", "slug": "marketing"}, {"id": 30, "name": "Sales", "slug": "sales"}, {"id": 23, "name": "Product", "slug": "product"}, {"id": 33, "name": "Business", "slug": "business"}, {"id": 24, "name": "Data", "slug": "data"}, {"id": 25, "name": "DevOps / Sysadmin", "slug": "devops"}, {"id": 26, "name": "Finance / Legal", "slug": "finance-legal"}, {"id": 27, "name": "Human Resources", "slug": "hr"}, {"id": 29, "name": "QA", "slug": "qa"}, {"id": 31, "name": "Teaching", "slug": "teaching"}, {"id": 32, "name": "Writing", "slug": "writing"}, {"id": 35, "name": "Medical / Health", "slug": "medical-health"}, {"id": 22, "name": "All others", "slug": "all-others"}

CATEGORIES = sorted([('software-dev', 'Software Development'), ('customer-support', 'Customer Service'), ('design', 'Design'),
('marketing', 'Marketing'), ('sales', 'Sales'), ('product', 'Product'), ('business', 'Business'), ('data', 'Data'), ('devops', 'DevOps'), ('finance-legal', 'Finance/Legal'), ('hr', 'Human Resources'), ('qa', 'Q/A'), ('teaching', 'Teaching'), ('writing', 'Writing'), ('medical-health', 'Medical/Health'), ('all-others', 'Others'), ('','All')], key=lambda x: x[1])

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()]) #need to figure oute email-validator????
    password = PasswordField('Password', validators=[Length(min=6)])
    location = StringField('(Optional) Location')
    bio = StringField('(Optional) Personal Bio')
    image_url = StringField('(Optional) Image URL')

class LoginForm(FlaskForm):
    """Form for logging existing user in"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class EditUserForm(FlaskForm):
    """Form to edit user info"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()]) #need to figure oute email-validator????
    password = PasswordField('Password', validators=[Length(min=6)])
    location = StringField('(Optional) Location')
    bio = StringField('(Optional) Personal Bio')
    image_url = StringField('(Optional) Image URL')

class SearchJobsForm(FlaskForm):
    """Form to search jobs"""
    search_term = StringField('(Optional) Search Term')
    category = SelectField('Category', 
        choices=CATEGORIES)
    company_name = StringField('(Optional) Company Name')
