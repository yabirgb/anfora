import datetime
import uuid

from peewee import *
from playhouse.shortcuts import model_to_dict

db = SqliteDatabase('zinat.db')

def createId():
    return str(uuid.uuid4())
    

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)

    
class Album(BaseModel):
    name = CharField()
    creted_date = DateTimeField(default=datetime.datetime.now)
    public = BooleanField(default=True)
    user = ForeignKeyField(User, backref='albums')

class Photo(BaseModel):
    title = CharField()
    identifier = CharField(default=createId, unique=True)
    upload_date = DateTimeField(default=datetime.datetime.now)
    public = BooleanField(default=True)
    user = ForeignKeyField(User, backref='photos')
    album = ForeignKeyField(Album, backref='albums', null=True)

    def __str__(self):
        return "{} - {} - {}".format(self.title, self.identifier, self.upload_date)

    def json(self):
        return model_to_dict(self)

def connect():
    db.connect()
    
def create_tables():
    tables = [User, Album, Photo]

    for table in tables:
        if not table.table_exists():
            table.create_table()
