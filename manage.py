import os, sys

def create():
    from sqlalchemy import Table
    import model
    for (name, table) in vars(model).iteritems():
        if isinstance(table, Table):
            table.create()

def drop():
    from sqlalchemy import Table
    import model
    for (name, table) in vars(model).iteritems():
        if isinstance(table, Table):
            if table.exists():
                table.drop()

def fill():
    from ink import add_and_type, add_comment

    add_and_type('Why we blog', 'blog', 'carry **moonbeams** home in a jar')
    add_and_type('Welcome to this blog', 'blog', 'would you //like// to swing on a star')
    blog = add_and_type('Who we are', 'blog', "you'd be [[better off]] than you are")
    comment = add_comment(blog, 'comment 1', 'your blog sucks')

def start(uri):
    if os.path.exists('content.db'):
        print "existing content.db, using it"
        run()
    else:
# this is all very naff. should be able to automate this
# with python code
        print "no content.db, getting from %s" % uri
        from butler import get

        db_content = get(uri)
        file = open('content.db', 'wb')
        file.write(db_content)
        file.close()

        run()

def dump():
    from butler import add

    db_content = open('content.db', 'rb').read()
    uri = add(db_content);
    print "dumped to %s" % uri

def run():
    import urls
    if os.environ.get("REQUEST_METHOD", ""):
        from wsgiref.handlers import BaseCGIHandler
        BaseCGIHandler(sys.stdin, sys.stdout, sys.stderr, os.environ) \
                .run(urls.load('urls.map'))
    else:
        os.environ = {}
        from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
        httpd = WSGIServer(('', 8080), WSGIRequestHandler)
        httpd.set_app(urls.load('urls.map'))
        print "Serving HTTP on %s port %s ..." % httpd.socket.getsockname()
        httpd.serve_forever()

if __name__ == '__main__':
    if 'drop' in sys.argv:
        drop()
    if 'create' in sys.argv:
        create()
    if 'fill' in sys.argv:
        fill()
    if 'start' in sys.argv:
        start(sys.argv[2])
    if 'run' in sys.argv:
        run()
    if 'dump' in sys.argv:
        dump()
