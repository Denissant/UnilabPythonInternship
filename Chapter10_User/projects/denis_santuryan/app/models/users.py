from flask_security import RoleMixin, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, backref

from app.database import db, Base
from app.tools.format_dob import calculate_age


class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


class UserModel(db.Model, UserMixin):
    """
    contains data about registered users
    each user may have posts linked to their profile
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False, index=True)
    name_first = db.Column(db.String)
    name_last = db.Column(db.String)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    phone = db.Column(db.String)
    sex = db.Column(db.String)
    dob = db.Column(db.Date)
    password = db.Column(db.String(255))
    age = db.Column(db.Integer)
    picture = db.Column(db.String)
    post = db.relationship('PostsModel', backref='usermodel', uselist=False)
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

    def __init__(self, username, name_first, name_last, email, phone, dob, sex, password, age=None, picture=None):
        self.username = username
        self.name_first = name_first
        self.name_last = name_last
        self.email = email
        self.phone = phone
        self.dob = dob
        self.sex = sex
        self.password = generate_password_hash(password)
        self.age = calculate_age(dob)
        self.picture = picture

    def __repr__(self):
        return f'ID: {self.id}. {self.username}'

    def check_password(self, password_raw):
        return check_password_hash(self.password, password_raw)

    @classmethod
    def find_by_username(cls, temp_username):
        return cls.query.filter_by(username=temp_username).first()

    @classmethod
    def find_by_email(cls, temp_email):
        return cls.query.filter_by(email=temp_email).first()


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
