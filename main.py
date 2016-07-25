import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from google.appengine.api import users

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.write(template.render(user))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
