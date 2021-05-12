from peewee import *
from .base import BaseModel
from bot import constants


class Science(BaseModel):
    name = CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Subject(BaseModel):
    science = ForeignKeyField(Science)

    name = CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name + ' | ' + self.science.name


class Interest(BaseModel):
    subject = ForeignKeyField(Subject)


class UserModel(BaseModel):
    """
        Fields: name, e-mail, interests, bio, department, degree-level + t_id, t_username.
    """
    t_id = IntegerField()

    t_username = CharField()

    name = CharField()

    email = CharField()

    interests = ForeignKeyField(Interest, backref='users')

    department = CharField(choices=constants.DEPARTMENT_OPTIONS)

    degree_level = CharField(choices=constants.DEGREE_LEVEL_OPTIONS)

    class Meta:
        db_table = 'Users'


class Problem(BaseModel):
    title = CharField()

    body = TextField()

    user = ForeignKeyField(UserModel)

    created_at = DateTimeField()

    topics = ForeignKeyField(Interest, backref='problems')

    is_closed = BooleanField(default=False)

    is_anonymous = BooleanField(default=False)


class Response(BaseModel):
    problem = ForeignKeyField(Problem, backref='responses')

    body = TextField()

    author = ForeignKeyField(UserModel)

    created_at = DateTimeField()

    is_anonymous = BooleanField(default=False)

    is_final = BooleanField(default=False)
