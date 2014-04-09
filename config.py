import logging
import os
from time import strftime, localtime

now = localtime()
now_f = strftime("%Y-%m-%d %H:%M:%S", now)

#logging config
timestamp = strftime("%Y-%m-%d-%H:%M:%S")
#logging_dir = os.path.join(os.path.dirname(__file__), 'logs/')

#delivery info
server = "delivery.plos.org"
port = 22
user = "web"
password = None

local_work_area = os.path.join(os.path.dirname(__file__), "workarea/")


#Email settings
# server settings
smtp_server_name = "sfexch02.plos.org"
smtp_server_port = 25

# email account settings
# simple email authentication. True for the plos relay.
# disregards email login/pass.
simple_email_auth = True

# email login/pass for simple_email_auth = False
email_sender = "webproduction@plos.org"
email_password = "stuff"

# email recipient setting, multiple addresses should be separated
# by commas ["jlabarba@plos.org", "jharney@plos.org"]
email_to = ["webproduction@plos.org"]