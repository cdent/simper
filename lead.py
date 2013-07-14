
"""
The hot lead that formats pages to whatever we like.
This is here in its own module because we want to 
a) be able to test it nice like (even though we don't yet)
b) work out ways to have the format() method come
   from multiple places, if we don't want creole or
   what have you
"""

from creoleparser.dialects import Creole10
from creoleparser.core import Parser

# FIXME: this url should come from config!!!
dialect = Creole10( wiki_links_base_url='/content/name/', wiki_links_space_char=' ' )
parser = Parser( dialect=dialect )

def format(content):
    """Turn creole text into html. For the time being does not
    support CamelCase. This should be fixed."""
    return parser(content)
