from butler import get

"""
The fetcher exists as an entry point for filtering,
caching and other crap for stuff acquired by the butler.
"""

def get_content(uri):
    """
Dig around in the closet, with the butler, and pull out
the requested content. We'll raise an error lower down
if things go wrong.
    """
    return get(uri)
