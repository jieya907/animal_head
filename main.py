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
import jinja2
import os
import urllib2
import face_detect

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# class HelloHandler(webapp2.RequestHandler):
#     def get(self):
#     	template_vars = {'name': self.request.get('name')}
#     	if(True):
#         	name = "CSSI Seattle"
#     	else:
#         	name = "CSSI Chicago"
#         template_vars = {"name": name}

#         template = jinja_environment.get_template('templates/hello.html')

#         self.response.out.write(template.render(template_vars))

# class MainHandler(webapp2.RequestHandler):
#     def get(self):
# 		template = jinja_environment.get_template('templates/main.html')
# 		self.response.out.write(template.render())

#     def post(self):
# 		self.response.out.write("Your answers have been submitted! You think you know Chicago?")

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render())

    def post(self):
        link = self.request.get('textline')
        face_detect.process_web(link)
        self.response.out.write("your link is " + link)


app = webapp2.WSGIApplication([
    ('/hello', HelloHandler),
    ('/main', MainHandler),
    ('/index', IndexHandler)
], debug=True)
