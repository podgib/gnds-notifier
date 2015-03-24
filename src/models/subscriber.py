from google.appengine.ext import db

class Subscriber(db.Model):
  email = db.EmailProperty(required=True)
  flavours = db.StringListProperty(required=True)
