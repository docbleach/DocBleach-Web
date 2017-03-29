import tornado.ioloop

from docbleach import application

if __name__ == "__main__":
  print("Listening on port 5000")
  application.listen(5000)
  tornado.ioloop.IOLoop.instance().start()
