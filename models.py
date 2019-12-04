# import * means import everything from peewee

from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('rivers.sqlite')


class RiverSystem(Model):
    name = CharField()

    class Meta:
        database = DATABASE

class RiverStation():
    name = CharField()

class User(Model, UserMixin):
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        db_table = 'users'
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([RiverSystem, User], safe=True)
    print("TABLES Created")
    DATABASE.close()

