from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User for site"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer, 
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    bio = db.Column(
        db.Text,

    )

    location = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )


    jobs = db.relationship('SavedJob')
    

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



class SavedJob(db.Model):
    """A job saved for later viewing"""

    __tablename__ = 'saved_jobs'

    id = db.Column(
        db.Integer, 
        primary_key=True,
    )

    job_id = db.Column(
        db.Integer,
    )

    job_title = db.Column(
        db.Text,
        nullable = False
    )

    company_name  = db.Column(
        db.Text
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    add_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    job_url = db.Column(
        db.Text
    )



    user = db.relationship('User')

    def __repr__(self):
        return f"<SavedJob id {self.id}: User {self.user_id} Title {self.job_title} Job ID: {self.job_id} Company Name {self.company_name}"

    @classmethod
    def serialize(self):
        """Returns a dict of saved job which can be converted to JSON"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_title': self.job_title,
            'job_id': self.job_id,
            'company_name': self.company_name
            }

def connect_db(app):
    """Connect this database to provided Flask app.
    """

    db.app = app
    db.init_app(app)