"""
Access content in a closet. Assumes closet is operational.
"""

import httplib2

poster_server = 'http://0.0.0.0:8000/'

# make these real exceptions with proper info and such
# 2.5 doesn't like string exceptions
post_error = 'unable to post'
get_error = 'unable to get'

def add(content):
    h = httplib2.Http()

    response, content = h.request(poster_server, 'POST', body=content, headers={'X-Closet-Cookie': 'holdem'})

    if response['status'] == '201':
        return response['location']
    else:
        raise post_error

def get(uri):
    h = httplib2.Http('.cache')

    response, content = h.request(uri, 'GET')

    if response['status'] == '200' or response['status'] == '304':
        return content
    else:
        raise get_error

if __name__ == '__main__':
    import sys, string
    if sys.argv:
        name = sys.argv[1]
        if name == 'add':
            content = sys.stdin.readlines()
            uri = add(string.join(content))
            print uri
