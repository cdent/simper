
import butler
import model
import producer
from simper import InvalidContent

default_type = 'text/plain'

def add_typed_to_page(name, type, content, to):
    """
    add the thing named name as type type to the thing named by to
    """
# if type is tag we want to not add, we only want to
# associate, if possible. But this means we are granting
# special code based knowledge to tag which is lame,
# we should clean this up eventually

    if type == 'tag':
        tag_id = _get_tag_id(name)
        if tag_id:
            associate_name_to_id(to, tag_id)
        else:
            tag_id = add_and_type(name, type, content)
            associate_name_to_id(to, tag_id)
    else:
        id = add_and_type(name, type, content)
        associate_name_to_id(to, id)

def _get_tag_id(tag_name):
    try:
        tag_id = producer.page_by_name(tag_name)['id']
    except TypeError:
        return
    return tag_id

def associate_name_to_id(to_name, id):
    try: 
        to_id = producer.page_by_name(to_name)['id']
        associate(to_id, id)
    except TypeError:
        pass


# REVIEW: This seems a bit awkward
def add_and_type(name, type, content):
    id = add(name, content)
    update_type(id, type)
    return id

def add_comment(blog, name, content):
    id = add_and_type(name, 'comment', content)
    associate(blog, id)

def add(name, content):
    return _revise(name, content)

def update(name, content):
    return _revise(name, content)

def update_type(revision_id, type):
    type_id = _type_list(type)
    if not type_id:
        type_id = _insert_type_list(type)

    _type_revision(revision_id, type_id)

    return type_id

def _type_revision(revision_id, type_id):
    it = model.type_table.insert()
    it.execute(revision_id = revision_id, type_id = type_id)

def _type_list(type):
    row = model.type_list_table.select(model.type_list_table.c.name==type) \
            .execute().fetchone()
    if row:
        return row.id
# row is NoneType here
    return row

def _insert_type_list(type):
    it = model.type_list_table.insert()
    result = it.execute(name = type)
    ids = result.last_inserted_ids()
    return ids[0]

def _revise(name, content):

    if len(name) == 0:
        raise InvalidContent, 'name must have length'

    ic = model.content_table.insert()
    ir = model.revision_table.insert()

    result = ir.execute(content_type = default_type,
            content_uri = butler.add(content))
    ids = result.last_inserted_ids()
    ic.execute(name = name, id = ids[0])
    return ids[0]

def associate(from_id, to_id):
    assoc = model.association_table.insert()
    assoc.execute(from_id = from_id, to_id = to_id)

if __name__ == '__main__':
    import sys, string
    if sys.argv:
        name = sys.argv[1]
        type = sys.argv[2]
        content = sys.stdin.readlines()
        add_and_type(name, type, string.join(content))


