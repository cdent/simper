from simper import render, get_request_content, HTTP303
from datetime import datetime
import ink
# XXX: this next busts the separation between ink and producer
# which seems wrong might be something wrong with model

@render('edit.html')
def add(environ, start_response):
    """
Look at posted stuff and use it for adding some content. 
Figure out the format of stuff and such.
    """
# ink.add(name, content)
    return

@render('')
def type_add(environ, start_response):
    """
Look at posted stuff and use it for adding some content. 
Figure out the format of stuff and such.
    """
    type = environ['wsgiorg.routing_args'][1]['type']
    to = environ['wsgiorg.routing_args'][1]['name']
    request_content = get_request_content(environ)

# if input isa dict, look for certain keys
    try:
        content = request_content['content'][0]
    except KeyError:
        content = request_content

    try:
        name = request_content['name'][0]
    except KeyError:
        name = str(datetime.utcnow())

    ink.add_typed_to_page(name, type, content, to)

# redirect to ourselves
    raise HTTP303, '/content/name/' + name

@render('edit.html')
def update(environ, start_response):
    """
Look at PUT stuff and use that to update an existing
entry. Since we are write once, this means updating
the content store with a new uri and metadata for the
same name.
    """
    name = environ['wsgiorg.routing_args'][1]['name']
# ink.add(name, content)
    return

