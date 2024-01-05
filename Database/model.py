from Database.db import db


class Credentials(db.Document):
    type = db.StringField(required=True)
    uname = db.StringField(required=True)
    password = db.StringField(required=True)


class Birdsdb(db.Document):
    ringno = db.StringField(primary_key=True)
    uname = db.StringField(required = True)
    specie = db.StringField(required=True)
    mutation = db.StringField(required=True)
    age = db.FloatField(required=True)
    gender = db.StringField(required=True)

class ForSale(db.Document):
    ringno = db.StringField(primary_key=True)
    uname = db.StringField(required=True)
    specie = db.StringField(required=True)
    mutation = db.StringField(required=True)
    age = db.FloatField(required=True)
    gender = db.StringField(required=True)
    price = db.IntField(required=True)