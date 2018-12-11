import tornado.ioloop
import tornado.web
import os
import json
import logging
import sys
import subprocess
import io
import base64

from logging.handlers import RotatingFileHandler

import requests

# logging configuration
LOG_FORMATTER = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
LOG_PATH = "logfile.log"
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
FILE_HANDLER = RotatingFileHandler(LOG_PATH, maxBytes=50*1024*1024)
FILE_HANDLER.setFormatter(LOG_FORMATTER)
CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
CONSOLE_HANDLER.setFormatter(LOG_FORMATTER)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

# Environment variables
APPLICATION_NAME = os.environ.get('APPLICATION_NAME')
SERVER_PORT = os.environ.get('SERVER_PORT')
MICROSERVICE_SUBSCRIPTION_ENABLED = os.environ.get('MICROSERVICE_SUBSCRIPTION_ENABLED')
C8Y_BASEURL = os.environ.get('C8Y_BASEURL')
C8Y_BASEURL_MQTT = os.environ.get('C8Y_BASEURL_MQTT')
C8Y_MICROSERVICE_ISOLATION = os.environ.get('C8Y_MICROSERVICE_ISOLATION')
C8Y_BOOTSTRAP_REGISTER = os.environ.get('C8Y_BOOTSTRAP_REGISTER')
C8Y_BOOTSTRAP_TENANT = os.environ.get('C8Y_BOOTSTRAP_TENANT')
C8Y_BOOTSTRAP_USER = os.environ.get('C8Y_BOOTSTRAP_USER')
C8Y_BOOTSTRAP_PASSWORD = os.environ.get('C8Y_BOOTSTRAP_PASSWORD')
C8Y_TENANT = os.environ.get('C8Y_TENANT')
C8Y_USER = os.environ.get('C8Y_USER')
C8Y_PASSWORD = os.environ.get('C8Y_PASSWORD')
MEMORY_LIMIT = os.environ.get('MEMORY_LIMIT')
PROXY_HTTP_HOST = os.environ.get('PROXY_HTTP_HOST')
PROXY_HTTP_PORT = os.environ.get('PROXY_HTTP_PORT')
PROXY_HTTP_NON_PROXY_HOSTS = os.environ.get('PROXY_HTTP_NON_PROXY_HOSTS')
PROXY_HTTPS_HOST = os.environ.get('PROXY_HTTPS_HOST')
PROXY_HTTPS_PORT = os.environ.get('PROXY_HTTPS_PORT')
PROXY_SOCKS_HOST = os.environ.get('PROXY_SOCKS_HOST')
PROXY_SOCKS_PORT = os.environ.get('PROXY_SOCKS_PORT')

# Authorization header for service user
SERVICE_AUTHENTHICATION_HEADER = 'Basic ' + base64.b64encode((C8Y_TENANT + '/' + C8Y_USER + ':' + C8Y_PASSWORD).encode()).decode()

'''
Simple handler to return hello world
'''
class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World")
        self.finish()
'''
Handler to return all environment variables of the container
'''
class EnvironmentHandler(tornado.web.RequestHandler):
    def get(self):
        environment = {
            'APPLICATION_NAME': APPLICATION_NAME,
            'SERVER_PORT': SERVER_PORT,
            'MICROSERVICE_SUBSCRIPTION_ENABLED': MICROSERVICE_SUBSCRIPTION_ENABLED,
            'C8Y_BASEURL': C8Y_BASEURL,
            'C8Y_BASEURL_MQTT': C8Y_BASEURL_MQTT,
            'C8Y_MICROSERVICE_ISOLATION': C8Y_MICROSERVICE_ISOLATION,
            'C8Y_BOOTSTRAP_REGISTER': C8Y_BOOTSTRAP_REGISTER,
            'C8Y_BOOTSTRAP_TENANT': C8Y_BOOTSTRAP_TENANT,
            'C8Y_BOOTSTRAP_USER': C8Y_BOOTSTRAP_USER,
            'C8Y_BOOTSTRAP_PASSWORD': C8Y_BOOTSTRAP_PASSWORD,
            'C8Y_TENANT': C8Y_TENANT,
            'C8Y_USER': C8Y_USER,
            'C8Y_PASSWORD': C8Y_PASSWORD,
            'MEMORY_LIMIT': MEMORY_LIMIT,
            'PROXY_HTTP_HOST': PROXY_HTTP_HOST,
            'PROXY_HTTP_PORT': PROXY_HTTP_PORT,
            'PROXY_HTTP_NON_PROXY_HOSTS': PROXY_HTTP_NON_PROXY_HOSTS,
            'PROXY_HTTPS_HOST': PROXY_HTTPS_HOST,
            'PROXY_HTTPS_PORT': PROXY_HTTPS_PORT,
            'PROXY_SOCKS_HOST': PROXY_SOCKS_HOST,
            'PROXY_SOCKS_PORT': PROXY_SOCKS_PORT
        }
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(environment))
        self.finish()

'''
Health endpoint to verify service is running
'''
class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        health = {
            'status': 'UP'
        }
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(health))
        self.finish()

'''
Handler to purposely kill the webserver
'''
class KillHandler(tornado.web.RequestHandler):
    def get(self):
        logging.error('Kill webserver')
        tornado.ioloop.IOLoop.current().stop()

'''
Handler to return the content of the log file
'''
class LogHandler(tornado.web.RequestHandler):
    def get(self):
        logging.debug('Get log')
        lines = self.get_argument('lines', default=100, strip=True)
        proc = subprocess.Popen(['tail', '-' + str(lines), LOG_PATH], stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
            self.write(line)
        self.finish()

'''
Handler to return the content of the log file
'''
class AverageHandler(tornado.web.RequestHandler):
    def get(self):
        logging.debug('Calculate average')
        credentials = self.request.headers.get('Authorization')

        if not verifyUserAccess(credentials, 'ROLE_AVERAGE_CALCULATION_READ'):
            raise tornado.web.HTTPError(403)

        fragmentType = self.get_argument('valueFragmentType', default='c8y_Temperature', strip=True)
        series = self.get_argument('valueFragmentSeries', default='T', strip=True)

        urlParams = {
            'valueFragmentType': fragmentType,
            'valueFragmentSeries': series,
            'source': self.get_argument('source', default=None, strip=True),
            'dateFrom': self.get_argument('dateFrom', default=None, strip=True),
            'dateTo': self.get_argument('dateTo', default=None, strip=True),
            'pageSize': 2000
        } 

        requestHeaders = {
            'Authorization': SERVICE_AUTHENTHICATION_HEADER
        }

        response = requests.get(C8Y_BASEURL + '/measurement/measurements', params=urlParams, headers=requestHeaders)
        measurements = response.json()['measurements']

        total = 0
        for measurement in measurements:
            total = total + measurement[fragmentType][series]['value']

        averageResponse = {
            'avg': total / len(measurements)
        }
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(averageResponse))
        self.finish()

'''
Verify incoming credentials for role
'''
def verifyUserAccess(credentials, role):
    requestHeaders = {
            'Authorization': credentials
        }
    response = requests.get(C8Y_BASEURL + '/user/currentUser', headers=requestHeaders)
    currentUserRoles = response.json()['effectiveRoles']
    roles = []

    for currentRole in currentUserRoles:
        roles.append(currentRole['id'])
    logging.debug(roles)

    if role in roles:
        return True
    else:
        return False

'''
Map handlers to REST paths
'''
def make_app():
    return tornado.web.Application([
        (r"/hello", HelloWorldHandler),
        (r"/environment", EnvironmentHandler),
        (r"/health", HealthHandler),
        (r"/kill", KillHandler),
        (r"/log", LogHandler),
        (r"/avg", AverageHandler),
    ])

# Generate tornado app
logging.debug('Generate app')
app = make_app()
# Expose app to port 80
logging.debug('Listen to port 80')
app.listen(80)
# Start the IO loop to handle incoming requests
logging.debug('Start IO loop')
tornado.ioloop.IOLoop.current().start()