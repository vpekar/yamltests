"""Extracts occurrences of twitter handles in text
"""

import re

P = re.compile(r'(?:^|\s)@(\w+)')


def extract(text):
    """Returns the first match as a string
    """
    return P.findall(text)[0]


class Extractor:
    
    def __init__(self):
        pass
    
    def extract(self, text):
        """Returns a list of matched strings
        """
        return P.findall(text)


class ExtractorWithInitKwargs:
    
    def __init__(self, lookup):
        """lookup is an object with names to be excluded
        """
        self.lookup = lookup
    
    def extract(self, text):
        """Returns a list of matched strings
        """
        return [x for x in P.findall(text) if not self.lookup.is_excluded(x)]
    
