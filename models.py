# import * means import everything from peewee

from peewee import *
from flask_login import UserMixin
from playhouse.db_url import connect
import os

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('rivers.sqlite')

#doesn't need to be numbers because only displaying
class RiverSystem(Model):
    river_section_number = CharField(primary_key=True)
    river_system = CharField(null=True, default='')
    station_name =  CharField(null=True, default='')
    time_of_reading = CharField(null=True, default='')
    gauge_height = CharField(null=True, default='')
    discharge = CharField(null=True, default='')
    lt_mean_flow = CharField(null=True, default='')
    lr_median_flow = CharField(null=True, default='')

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
