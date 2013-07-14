from simper import render, DataNotFound
from sqlalchemy import text
from fetcher import get_content
from lead import format
import model
import producer

@render('list.html')
def list(environ, start_response):
    pages = producer.list_names()
    return dict(pages=pages, title='All Content')

@render('list.html')
def type_list(environ, start_response):
    type = environ['wsgiorg.routing_args'][1]['type']
    pages = producer.list_names_by_type(type)
    return dict(pages=pages, title='All %s Content' % type)

@render('list.html')
def type_list_for_name(environ, start_response):
    type = environ['wsgiorg.routing_args'][1]['type']
    name = environ['wsgiorg.routing_args'][1]['name']
    pages = producer.list_names_by_type_for_name(type, name, 'DESC')
    return dict(pages=pages, title='All %s on %s' % (type, name))

@render('list.html')
def list_revisions(environ, start_response):
    name = environ['wsgiorg.routing_args'][1]['name']
    pages = producer.revisions_by_name(name)
    return dict(pages=pages, title='Revisions for %s' % name)

@render('page.html')
def content(environ, start_response):
    name = environ['wsgiorg.routing_args'][1]['name']
    page = producer.page_by_name(name)
    if not page:
        return _incipient_page(name)
    pages = producer.revisions_by_name(name)
    return _display_page(page, pages[0]['id'], name, pages[1:])

@render('page.html')
def content_revision(environ, start_response):
    name = environ['wsgiorg.routing_args'][1]['name']
    id = environ['wsgiorg.routing_args'][1]['id']
    page = producer.page_by_id(name, id)
    return _display_page(page, id, 'Revision id %s of %s' % (id, name), [])

def _display_page(page, id, title, pages):
    try:
        content = get_content(page['content_uri'])
        comments = producer.list_names_by_type_for_name('comment', page['name'], 'ASC')
        tags = producer.list_names_by_type_for_name('tag', page['name'], 'ASC')
        associates = producer.revisions_for_associate(id)
        _fill_comments(comments)
        return dict(page=page, title=title, text=format(content), \
                pages=pages, comments=comments, tags=tags, associates=associates)
    except TypeError, e:
        import traceback
        traceback.print_exc()
        raise DataNotFound

def _incipient_page(name):
    return dict(page={'name': name}, title=name, text="Page does not exist. Editing soon.")

def _fill_comments(comments):
    for comment in comments:
        name = comment['name']
        uri = comment['content_uri']
        comment['content'] = format(get_content(uri))
        comment['associates'] = producer.list_names_by_type_for_name('comment', name, 'ASC')

@render('list.html')
def date(environ, start_response):
    pages = producer.list_names()
    return dict(pages=pages, title='By Date')

