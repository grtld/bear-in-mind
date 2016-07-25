import webapp2
import jijna2
import os

from google.appengine.ext import ndb


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

>>>>>>> fe5badf1fef66fc22f70a7b2d292d01940ef86a2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
