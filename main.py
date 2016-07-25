import webapp2
import jinja2
import os
import logging

from google.appengine.ext import ndb
from google.appengine.api import users


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


#model for message
class Reminder(ndb.Model):
    title = ndb.TextProperty()
    description = ndb.TextProperty()

class User(ndb.Model):
    email = ndb.StringProperty()
    reminders = ndb.StringProperty(repeated=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        #show a list of the reminders
        #reminder = Reminder.query().fetch()

        #render response
        #template_values= {'reminder':reminder}

        #template = jinja_environment.get_template('home.html')
        self.response.write(user)

    #post method that adds reminder into database
    def post(self):
        #get reminder from form
        reminder = self.request.get('reminder')

        #saves & puts the reminder from form into the database
        new_reminder = Reminder(reminder = reminder)
        new_reminder.put()

        #shows the main page after you press submit
        self.redirect("/")
class AddHandler(webapp2.RequestHandler):
    def get(self):
        #render a response
        template = jinja_environment.get_template('add.html')
        self.response.write(template.render())

    def post(self):
        #get reminder from form
        title = self.request.get('title')
        description = self.request.get('description')
        frequency = self.request.get('frequency')

        #put the reminders from form into the database
        new_reminder = Reminder(title = title,description = description,frequency = frequency)
        new_reminder.put()

        #shows the home page after you press submit
        self.redirect("/")
app = webapp2.WSGIApplication([
    ('/add', AddHandler),
    ('/', MainHandler)
], debug=True)
