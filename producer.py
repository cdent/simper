from butler import get
from sqlalchemy import text
import model

def _pages_from_rows(rows):
    pages = []
    for row in rows:
        pages.append(_page_from_row(row))

    return pages

def list_names():
    sql = text("""
        SELECT 0 as id, revision.id as revision, content.name, max(revision.mod_time) as mod_time, count(revision.id) as count
            FROM content, revision
                WHERE content.id = revision.id
                GROUP BY content.name
                ORDER BY revision.mod_time DESC
    """)
    rows = model.content_table.bind.execute(sql)
    return _pages_from_rows(rows)

def list_names_by_type(type):
    sql = text("""
        SELECT 0 as id, revision.id as revision, content.name, max(revision.mod_time) as mod_time, count(revision.id) as count
            FROM content, revision, type, type_list
                WHERE content.id = revision.id
                AND revision.id = type.revision_id
                AND type_list.id = type.type_id
                AND type_list.name = :intype
                GROUP BY content.name
                ORDER BY revision.mod_time DESC
    """)
    rows = model.content_table.bind.execute(sql, intype = type)
    return _pages_from_rows(rows)

# XXX this gets all the comments, even those that might have 
# been deleted, because the inner select returns multiple values
# which means, if we use this some other places we don't have
# to migrate tags and comments ahead...
# hmm
def list_names_by_type_for_name(type, name, sort):
    sql = text("""
        SELECT 0 as id, revision.id as revision, revision.content_uri, content.name, max(revision.mod_time) as mod_time, count(revision.id) as count
            FROM content, revision, type, type_list, association
                WHERE association.from_id IN
                    (SELECT content.id FROM content WHERE content.name = :inname)
                AND association.to_id = revision.id
                AND revision.id = content.id
                AND type.revision_id = revision.id
                AND type.type_id = type_list.id
                AND type_list.name = :intype
                GROUP BY content.name
                ORDER BY revision.mod_time 
    """)
    sql = "%s %s" % (sql, sort)
    rows = model.content_table.bind.execute(sql, intype = type, inname = name)
    return _pages_from_rows(rows)

# if we need more than name and mod_time we might need to use this sql instead
#     SELECT content.name, revision.mod_time
#         FROM content, revision
#         WHERE content.id = revision.id AND revision.id = (
#             SELECT revision.id
#                 FROM revision, content c2
#                 WHERE c2.name=content.name
#                 AND revision.id = c2.id
#                 ORDER BY revision.mod_time DESC LIMIT 1
#     )

def revisions_for_associate(associate_id):
    sql = text("""
     SELECT revision.id, revision.content_uri, type_list.name as type, revision.mod_time, content.name, 0 as count
     FROM revision, association, content, type, type_list
     WHERE association.to_id=:inrev
     AND revision.id=association.from_id
     AND content.id=revision.id
     AND type.type_id=type_list.id
     GROUP By revision.id
    """)
    rows = model.content_table.bind.execute(sql, inrev=associate_id, intype=type)
    return _pages_from_rows(rows)

def revisions_by_name(name):
    sql = text("""
    SELECT revision.id, revision.content_uri, revision.mod_time, content.name, 0 as count
        FROM content, revision WHERE name=:inname AND content.id=revision.id ORDER BY mod_time DESC
    """)
    rows = model.content_table.bind.execute(sql, inname=name)
    return _pages_from_rows(rows)

def _page_from_row(row):
    try:
        page = dict(zip(row.keys(), row.values()))
        if page.get('revision'):
            page['associates'] = revisions_for_associate(page['revision'])
        return page
    except AttributeError:
        return 

def page_by_name(name):
    sql = text("""
    SELECT revision.id, revision.content_uri, revision.mod_time, content.name
        FROM content,revision WHERE name=:inname AND content.id=revision.id ORDER BY mod_time DESC LIMIT 1
    """)
    row = model.revision_table.bind.execute(sql, inname=name).fetchone()

    return _page_from_row(row)


def page_by_id(name, id):
    sql = text("""
    SELECT revision.content_uri, revision.mod_time, content.name
        FROM content,revision WHERE content.name=:inname AND revision.id=:inid AND content.id=revision.id
    """)
    row = model.revision_table.bind.execute(sql, inname=name, inid=id).fetchone()

    return _page_from_row(row)
