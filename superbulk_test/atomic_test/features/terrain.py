from lettuce import *

from utils import before_all, set_post_data, make_request

@before.all
def set_browser():
    before_all()

@step(r'the post data is "(.*)"')
def access_url(step, data):
    set_post_data(data)

@step(r'I post the data to "(.*)"')
def post_data(step, url):
    make_request(url, world.post_data)