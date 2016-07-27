import webapp2
import jinja2
import os
import logging

from google.appengine.ext import ndb
from google.appengine.api import users
from datetime import date
import datetime


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

#model for message
class User(ndb.Model):
    email = ndb.StringProperty()
    #a method that return the key url for a user when called
    def url(self):
        url = '?key=' + self.key.urlsafe()
        return url

class Reminder(ndb.Model):
    title = ndb.TextProperty()
    description = ndb.TextProperty()
    frequency = ndb.IntegerProperty()
    month = ndb.IntegerProperty()
    day = ndb.IntegerProperty()
    year = ndb.IntegerProperty()
    user_key = ndb.KeyProperty(kind=User)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        user = str(user)
        if User.query(User.email == user).get() == None:
            new_user = User(email=user)
            new_user.put()

        #show a list of the reminders
        user = User.query(User.email == user).get()
        urlsafe_key = user.key.urlsafe()
        key = ndb.Key(urlsafe=urlsafe_key)

        #get list of reminders from specific user
        reminders = Reminder.query(Reminder.user_key == key).fetch()

        # algorithm for what reminders to show for today
        #empty list of the reminders needed to show today
        todays_reminders = []
        upcoming_reminders = []
        #get today's date
        today = datetime.datetime.now()
        #loop through all the reminders
        for reminder in reminders:
            #today's date
            d0 = date(today.year, today.month, today.day)
            #date of reminder
            d1 = date(reminder.year, reminder.month, reminder.day)
            delta = d0 - d1
            difference = delta.days
            #if today's day date is equal to dataTime for the reminder + frequency, add to the list of today's reminders
            if  difference % reminder.frequency == 0:
                #make the reminder for today equal to the current reminder from the list
                today_reminder = reminder
                #add the reminder to the list of the reminders that are going to be posted for today
                todays_reminders.append(today_reminder)
            else:
                upcoming_reminders.append(reminder)

        #render response
        template_values= {'todays_reminders':todays_reminders, 'upcoming_reminders':upcoming_reminders, 'user':user, 'logout_url':logout_url}
        template = jinja_environment.get_template('home.html')
        self.response.write(template.render(template_values))

class ReminderHandler(webapp2.RequestHandler):
    def get(self):
        #get user key
        urlsafe_key = self.request.get('key')

        #render a response
        template = jinja_environment.get_template('add.html')
        self.response.write(template.render())

    def post(self):
        #get reminder from form
        title = self.request.get('title')
        description = self.request.get('description')
        frequency = self.request.get('frequency')
        month = int(self.request.get('month'))
        day = int(self.request.get('day'))
        year = int(self.request.get('year'))
        urlsafe_key = self.request.get('key')
        key = ndb.Key(urlsafe=urlsafe_key)

        #put the reminders from form into the database
        new_reminder = Reminder(title=title, description=description, frequency=int(frequency), month=month, day=day, year=year, user_key=key)
        new_reminder.put()

        #shows the home page after you press submit
        self.redirect("/home")

class RemoveHandler(webapp2.RequestHandler):
    def get(self):
        #get user key
        urlsafe_key = self.request.get('key')
        key = ndb.Key(urlsafe=urlsafe_key)

        #get list of reminders from specific user
        reminders = Reminder.query(Reminder.user_key == key).fetch()
        #render a response
        template_vals = {'reminders': reminders}
        template = jinja_environment.get_template('remove.html')
        self.response.write(template.render(template_vals))

    def post(self):
        urlsafe_key = self.request.get('key')
        key = ndb.Key(urlsafe=urlsafe_key)
        #reminders = Reminder.query(Reminder.user_key == key).fetch()
        reminder = self.request.get('reminder')
        '''
        reminder_key = ndb.Key(urlsafe=rem_reminder)
        reminders.reminder_key.delete()
        #shows the home page after you press submit
        self.redirect("/removereminder?="+urlsafe_key)
        '''
        self.response.write(reminder)

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('login.html')
        self.response.write(template.render())

        """from twilio.rest import TwilioRestClient

        account_sid = "AC0956d071691cb608aabfa3a73b2592d6" # Your Account SID from www.twilio.com/console
        auth_token  = "6756531644d0e1845a63c235473b83dc"  # Your Auth Token from www.twilio.com/console

        client = TwilioRestClient(account_sid, auth_token)

        message = client.messages.create(body="Daily Reminder: {{user.reminder}}",
            to="+1{user.phone}",    # Replace with your phone number
            from_="+15104582359") # Replace with your Twilio number

        print(message.sid)"""

#    def post(self):
#        self.redirect('/')

app = webapp2.WSGIApplication([

    ('/addreminder', ReminderHandler),
    ('/home', MainHandler),
    ('/removereminder', RemoveHandler),
    ('/', LoginHandler)
], debug=True)
