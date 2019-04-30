import urllib.request,json
from .models import User
import requests

def configure_request(app):
    global base_url
    base_url = app.config['QUOTES_API_BASE_URL']

def get_quote():
   '''
   function that gets the json response to the url request
   '''
   url = 'http://quotes.stormconsultancy.co.uk/random.json'
   pos = requests.get(url)
   posts = pos.json()
   return posts