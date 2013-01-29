class Lookup:
    """A class containing usernames not to be extracted
    """
    def __init__(self):
        self.excluded_names = ['username']
     
    def is_excluded(self, name):
        return True if name in self.excluded_names else False

# a dict, where each key is the name of a class being tested and the value is kwargs 
# to be passed to the __init__ method of the class
init_kwargs = {'ExtractorWithInitKwargs': {
                                    'lookup': Lookup()
                                    },
               }

