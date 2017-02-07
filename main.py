#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

def signup(err1,err2,err3):
    usernamelbl = "<label>Username:</label>"
    usernameinput = "<input type = 'text' name = 'username'/>"
    passwordlbl = "<label>Password:</label>"
    passwordinput = "<input type = 'password' name = 'password'/>"
    verifypasswordlbl = "<label>Verify Password:</label>"
    verifypasswordinput = "<input type = 'password' name = 'verifypassword'/>"
    emaillbl = "<label>Email(Optional):</label>"
    emailinput = "<input type = 'text' name = 'email'/>"
    usernameerr = err1
    passworderr = err2
    emailerr = err3

    submit = "<input type = 'submit'>"

    form = ("<form method ='post' action='/'>" +
            usernamelbl + usernameinput + err1 + "<br>" +
            passwordlbl + passwordinput + err2 + "<br>" +
            verifypasswordlbl + verifypasswordinput +"<br>" +
            emaillbl + emailinput +err3 + "<br>" +
            submit
            + "</form>")
    header = "<h2>Signup</h2>"
    return header + form

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return email and EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = signup("","","")
        self.response.write(content)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verifypassword = self.request.get("verifypassword")
        email = self.request.get("email")
        have_error =False
        err_username = ''
        err_password = ''
        err_email = ''
        if valid_username(username):
            err_username = ''
        else:
            have_error = True
            err_username ="Invalid username entered"

        if valid_password(password) :
            if valid_password(verifypassword) and (password == verifypassword):
                err_password = ''
            else:
                have_error = True
                err_password = "Password does not match"
        else:
            err_password = "Invalid Password"
            have_error = True

        if valid_email(email):
            err_email = ''
        else:
            err_email = "Invalid Email"
            have_error = True


        if have_error:
            content = signup(err_username,err_password,err_email)
            self.response.write(content)
        else:
            self.redirect('/welcome?username=' + username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        content = "Welcome " + username + " Thanks!"
        self.response.write(content)

        #self.render("\welcome.html")
        #if valid_username(username):
            #self.response.redirect('welcome.html',username = username)
            #self.render('welcome.html',username = username)
        #else:
            #self.redirect('/signup')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome',Welcome)
    #('/unit2/welcome', Welcome)
], debug=True)
