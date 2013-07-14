import os
import neo_cgi
import neo_util
import neo_cs
from cgi import parse_qs
# FIXME: this introduces a dependency on wsgiref at a weird level
from wsgiref.util import request_uri


extensions = {
    'html': 'text/html',
    'atom': 'application/atom+xml'
}

# keep the stylesheet in the closet?
stylesheet_uri = 'http://localhost:8002/fb7ee928834540bb88c1c82cc9e18e30'

class ValuedException( Exception ):
    def __init__(self, value):
        self.value = value
    def __str__(self):
       return repr(self.value)

class DataNotFound( Exception ):
    pass

class HTTP303( ValuedException ):
    pass
 
class InvalidContent( ValuedException ):
    pass

# borrows from turbogears.expose
def render(template_file):
    """
Create a decorator that will take the dict returned from the 
method being decorated and use it to fill in the template
named in template_file.

This needs to be updated so it does content negotiation.
The wrapped method still returns just data, but sometime
we might json, atom, html, text, etc. This could mean
template handling, it could mean json processor, whatever.

Other option is a more content negotation style of handling
in Selector. This would make the mapping more like what
is done in REST::Application.

I'm inclined to do something in decorators and see how
that goes. That may the mapping is only about methods
and URIs: that first line of the HTTP request.
"""
    def entangle(f):
        def render(environ, start_response, *args, **kwds):
            output = _render(f, template_file, environ, \
                    start_response, args, kwds)
            return output
        return render
    return entangle

def get_request_content(environ):
    """
Look at the request and return the input.
Should this be a string, a python dict, what?
    """
    length = int(environ['CONTENT_LENGTH'])
    input = environ['wsgi.input']
    request_content = input.read(length)

    content_type = environ.get('CONTENT_TYPE', '') 
    content_type = content_type.split(';')[0]
    if content_type and content_type == 'application/x-www-form-urlencoded':
       return parse_qs(request_content, keep_blank_values=1)
    else:
       return request_content

def _render(f, template_file, environ, start_response, *args, **kwds):

    # call our original function with original args
    try:
        results = f(environ, start_response)

        template_name, ext = template_file.split(".")
        contenttype = "text/html"
        if len(ext) > 1 and (ext[1] in extensions):
            contenttype = extensions[ext[1]]

        hdf = neo_util.HDF()
        _set(hdf, '', results)
        hdf.setValue('style', stylesheet_uri)

        # shove the results into the template
        clearsilver = neo_cs.CS(hdf)
        clearsilver.parseFile(os.path.join('templates', template_name + '.cs'))

        # XXX where is our error handling?
        start_response("200 OK", [('Content-Type', contenttype)])
        return [clearsilver.render()]
    except DataNotFound:
        start_response("404 Not Found", [('Content-Type', 'text/plain')])
        return ['404 Error, Content not found']
    except HTTP303, e:
        url = str(e.value)
        if not url.startswith(('http', '/')):
            url = request_uri(environ) + url
        start_response("302 Found", [('Location', url)])
        return ['Redirect to url']
    except InvalidContent, e:
        start_response("500 Server Error", [])
        return [e.value]
        

# this is borrowed from 
# http://www.premolo.org/projects/base/browser/trunk/src/premolo/clearsilver.py
# That code is licensed under GPL 2. Will need to reconcile that at some
# point.

def _set(hdf, name, value):

    if name is None:
        name = ''

    escape = lambda a: a
    
    def convertDict(value):
        if isinstance(value, dict):
            return value.iteritems()
    
    def convertEnumerable(value):
        try:
            return enumerate(value)
        except TypeError:
            pass
    
    setValue = hdf.setValue
    encoding = 'utf-8'
    convs = convertDict, convertEnumerable
    boolean = tuple( i.encode(encoding) for i in '01' )
    
    def add_value(prefix, value):
        if value is None:
            pass
        elif value in (True, False):
            setValue( prefix, boolean[value] )
        elif isinstance(value, unicode):
            setValue( prefix, escape(value).encode(encoding) )
        elif isinstance(value, str):
            setValue( prefix, escape(value) )
        else:
            # converters must return (key, item) tuples.
            for conv in convs:
                enum = conv(value)
                if enum is not None:
                    if prefix:
                        for key, item in enum:
                            add_value('%s.%s' % (prefix, key), item)
                    else:
                        for key, item in enum:
                            add_value(key, item)
                    break
            else:
                value = unicode(value)
                add_value(prefix, value)
    
    add_value(name, value)

