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
    
    def __init__(self, excluded_names):
        self.excluded_names = excluded_names
    
    def extract(self, text):
        """Returns a list of matched strings
        """
        return [x for x in P.findall(text) if x not in self.excluded_names]
    
