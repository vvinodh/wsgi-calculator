"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
from wsgiref.simple_server import make_server

def web_header(func, *args):
    body = "<h2>" + func.title() + " Function</h2>"
    body += "\r\n" * 2
    body += "<p>When you " + func + " "
    body += " and ".join(args)
    body += " you get "
    return body

def landing_page():
    body = "<h2>Welcome to the Calculator Page</h2>"
    body += "\r\n" * 2
    body += "To return a calculation simply enter a mathmatical function (add,"
    body += "subtract, multiply, divide) as the first segment of the path and the"
    body += "you would like to perform the function on in order separated by slashes"
    body += "<br>" * 2
    body += 'For example <a href="http://localhost:8080/add/4/6">localhost:8080/add/4/6</a> you should see a page"'
    body += "detailing the operation and giving you an answer of 10"
    return body

def do_math(func, *args):
    args_list = list(args)
    return_value = float(args_list.pop(0))
    if func == "add":
        for arg in args_list:
            return_value = return_value + float(arg)
    elif func == "subtract":
        for arg in args_list:
            return_value = return_value - float(arg)
    elif func == "multiply":
        for arg in args_list:
            return_value = return_value * float(arg)
    elif func == "divide":
        for arg in args_list:
            return_value = return_value / float(arg)
    return str(return_value)

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    path_info = path.split("/")
    func = path_info[1]
    args = path_info[2:]
    return func, args

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        if path == "/":
            body = landing_page()
        else:
            func, args = resolve_path(path)
            body = web_header(func, *args)
            body += do_math(func, *args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error you!"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()