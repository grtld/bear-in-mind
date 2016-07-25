import webapp2
import jinja2
import os

from google.appengine.ext import ndb


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

#model for message
class Reminder(ndb.Model):
    reminder = ndb.TextProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #show a list of the reminders
        reminder = Reminder.query().fetch()

        #render response
        template_values= {'reminder':reminder}

        template = jinja_environment.get_template('home.html')
        self.response.write(template.render(template_values))

    #post method that adds reminder into database
    def post(self):
        #get reminder from form
        reminder = self.request.get('reminder')

        #saves & puts the reminder from form into the database
        new_reminder = Reminder(reminder = reminder)
        new_reminder.put()

        #shows the main page after you press submit
        self.redirect("/")

#add time stamp and use it to order messages
#log in and log out links

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
