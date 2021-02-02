from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

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

    header_image_url = db.Column(
        db.Text,
        default="/static/images/lockers.png"
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


    job_title = db.Column(
        db.Text,
        nullable = False
    )

    # description = db.Column(
    #     db.Text,
    #     nullable = False
    # )

    # location = db.Column(
    #     db.Text,
    #     nullable = False
    # )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    user = db.relationship('User')

    def __repr__(self):
        return f"<SavedJob id {self.id}: User {self.user_id} Title {self.job_title}"

    @classmethod
    def serialize(self):
        """Returns a dict of saved job which can be converted to JSON"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_title': self.job_title
            }

def connect_db(app):
    """Connect this database to provided Flask app.
    """

    db.app = app
    db.init_app(app)