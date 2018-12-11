import tornado.ioloop
import tornado.web
import os
import json

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
Map handlers to REST paths
'''
def make_app():
    return tornado.web.Application([
        (r"/hello", HelloWorldHandler),
        (r"/environment", EnvironmentHandler),
    ])

# Generate tornado app
app = make_app()
# Expose app to port 80 
app.listen(80)
# Start the IO loop to handle incoming requests
tornado.ioloop.IOLoop.current().start()