# from csv import DictReader
from app import db
from models import User, SavedJob



db.drop_all()
db.create_all()
