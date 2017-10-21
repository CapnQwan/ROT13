import os

import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

class Handler(webapp2.RequestHandler):
	def render(self, template ,**kw):
		self.response.out.write(render_str(template, **kw))

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

class MainPage(Handler):
	def get(self):
		self.render('index.html')

	def post(self):
		new_text = ''
		text = self.request.get('text')
		if text:
			for c in text:
				n = ord(c)
				if n <= 109 and n >= 97:
					n = n + 13
				elif n >= 110 and n <= 122:
					n = n - 13
				elif n <= 77 and n >= 65:
					n = n + 13
				elif n >= 78 and n <= 90:
					n = n - 13
				else:
					n = n
				new_text += chr(n)
		self.render("index.html", text = new_text)

app = webapp2.WSGIApplication([('/rot13', MainPage)
								],
								debug=True)