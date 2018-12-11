import tornado.ioloop
import tornado.web

'''
Simple handler to return hello world
'''
class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World")
        self.finish()

'''
Map handlers to REST paths
'''
def make_app():
    return tornado.web.Application([
        (r"/hello", HelloWorldHandler),
    ])

# Generate tornado app
app = make_app()
# Expose app to port 80 
app.listen(80)
# Start the IO loop to handle incoming requests
tornado.ioloop.IOLoop.current().start()