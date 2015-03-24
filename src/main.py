#!/usr/bin/env python
from google.appengine.api import mail

import webapp2
import jinja2
import os

from models.subscriber import Subscriber

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class SubscribeHandler(webapp2.RequestHandler):
  def get(self):
    template = jinja_environment.get_template('templates/subscribe.html')
    self.response.out.write(template.render({}))

  def post(self):
    email = self.request.get("email")
    flavour = self.request.get("flavour")
    subscribers = Subscriber.all().filter('email =', email).fetch(1)
    if len(subscribers) == 0:
      subscriber = Subscriber(email = email, flavours = [flavour.lower()])
    else:
      subscriber = subscribers[0]
      subscriber.flavours.append(flavour.lower())
    subscriber.put()
    template = jinja_environment.get_template('templates/subscribed.html')
    self.response.out.write(template.render({'flavour':flavour}))

class UnsubscribeHandler(webapp2.RequestHandler):
  def get(self):
    template = jinja_environment.get_template('templates/unsubscribe.html')
    self.response.out.write(template.render({}))

  def post(self):
    email = self.request.get("email")
    subscribers = Subscriber.all().filter('email =', email).run()
    for subscriber in subscribers:
      subscriber.delete()
    template = jinja_environment.get_template('templates/unsubscribed.html')
    self.response.out.write(template.render({}))

app = webapp2.WSGIApplication(
  [('/', SubscribeHandler),
    ('/subscribe', SubscribeHandler),
    ('/unsubscribe', UnsubscribeHandler)], debug=True)