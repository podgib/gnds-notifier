import logging
import jinja2
import webapp2
import os
from scraper.scraper import Scraper
from models.subscriber import Subscriber
from google.appengine.api import taskqueue
from google.appengine.api import mail

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class ScrapeHandler(webapp2.RequestHandler):
  def get(self):
    self.post()

  def post(self):
    logging.info('Running ScrapeHandler')
    scraper = Scraper()
    scraper.scrape("http://www.gdcafe.com/website/index.php/Flavours")
    subscribers = Subscriber.all().run()
    for s in subscribers:
      danver_flavours = []
      delila_flavours = []
      davis_flavours = []
      for f in s.flavours:
        if f in scraper.danver_flavours:
          danver_flavours.append(f)
        if f in scraper.davis_flavours:
          davis_flavours.append(f)
        if f in scraper.delila_flavours:
          delila_flavours.append(f)

      if len(danver_flavours) == 0 and len(delila_flavours) == 0 and len(davis_flavours) == 0:
        continue

      params={'email':s.email, 'danver':danver_flavours, 'davis':davis_flavours, 'delila':delila_flavours}
      taskqueue.add(url='/worker/email', params=params, queue_name='email', countdown=0)
      logging.info('Submitted task to email ' + s.email)

    taskqueue.add(url='/worker/scrape', countdown=86400)
    logging.info('Finished ScrapeHandler')

class EmailHandler(webapp2.RequestHandler):
  def post(self):
    email = self.request.get('email')
    davis = self.request.get_all('davis')
    danver = self.request.get_all('danver')
    delila = self.request.get_all('delila')

    template = jinja_environment.get_template('templates/email.html')
    subject = "G&D's Flavour Notification"
    message = mail.EmailMessage(sender="G&D's flavour notifier <no-reply@gnds-notifier.appspotmail.com>", subject=subject)
    message.to = email
    message.body = template.render({'email': email, 'davis':davis, 'danver':danver, 'delila':delila})
    logging.info(message.body)
    logging.info("Sending email to " + email)
    message.send()

app = webapp2.WSGIApplication(
  [('/worker/scrape', ScrapeHandler),
   ('/worker/email', EmailHandler)], debug=True)


