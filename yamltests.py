"""A nose plugin for tests written in YAML (.yml). The format of tests:

path.to.myModule:
    myFunctionInMyModule:
        description: "Extract twitter handle"
        text: "... @username ..."
        expected: "username"
    myClassInMyModule:
        myMethod:
            description: "Extract twitter handle"
            text: "... @username ..."
            expected: ["username"]

Note that the function/method being tested can output either a string or a 
list. The expected value can be either a string or a list. 
- If the expected value is a string and actual value is a string, assertEqual
is used.
- If the expected value is a string and actual value is a list, assertIn is 
used.
- If the expected value is a list and actual value is a list, assertListEqual
is used.

Notes:
- If the yaml file contains comma-separated module name (SomePackage.SomeModule)
then the __init__.py file inside SomePackage should explicitly import all
modules (see the __init__.py file in the example folder)

Created on 21 Jan 2013

@author: vpekar
"""


import sys, os, logging, unittest
from nose.plugins.base import Plugin
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


LOGGER = logging.getLogger('nose.plugins.yamltests')


def do_import(name):
    """Import a module specified as a string
    """
    components = name.split('.')
    module = __import__(components[0])
    for comp in components[1:]:
        module = getattr(module, comp)
    return module
     

class Case(unittest.TestCase):
    """A test case to be created at run time
    """
    
    input = ''
    expected = None
    actual = None
    desc = ''
    func_name = None
    class_name = None
    file_name = None
    
    def setUp(self):
        if self.class_name:
            self.instance = globals()[self.class_name]()
     
    def runTest(self):
        
        if self.class_name:
            func = self.instance.__class__.__dict__[self.func_name]
            self.actual = func(self.instance, self.input)
        else:
            func = globals()[self.func_name]
            self.actual = func(self.input)
      
        msg_vars =  (self.file_name, self.desc, self.actual, self.expected)
        
        if isinstance(self.expected, list) and isinstance(self.actual, list):
            msg = "%s: %s\n\tActual: %s\n\t!=\n\tExpected %s" % msg_vars
            self.assertListEqual(self.actual, self.expected, msg)
        elif isinstance(self.expected, str):
            if isinstance(self.actual, list):
                msg = "%s: %s\n\tActual %s does not have Expected \"%s\""
                self.assertIn(self.expected, self.actual, msg  % msg_vars)
            elif isinstance(self.actual, str):
                msg = "%s: %s\n\tActual: \"%s\" != Expected \"%s\"" % msg_vars
                self.assertEqual(self.actual, self.expected, msg)
            else:
                raise TypeError("Actual value should be a list or a "
                    "string. Got %s (%s)" % (type(self.actual), self.file_name))
        else:
            raise TypeError("Either both actual and expected values should "
                "be lists, or expected value should be a string. Got actual "
                "type %s, expected type %s (%s)" % (type(self.actual), 
                type(self.expected), self.file_name))


class YamlTestParser:
    """Parses YAML files and creates test cases
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_testcase(self, case_data, func_name, file_name,
                      class_name=None):
        """Construct a test case
        """
        case = Case()
        case.func_name = func_name
        case.input = case_data['text']
        case.desc = case_data['description']
        case.expected = case_data['expected']
        case.class_name = class_name
        case.file_name = file_name
        return case

    def get_cases(self, fname):
        """Yield TestCases found in the file.
        """
        for module_name, module_tests in self.parse_yaml(fname).items():
            
            for class_name, class_tests in module_tests.items():
            
                # import the class/function
                full_name = "%s.%s" % (module_name, class_name)
                globals()[class_name] = do_import(full_name)
                
                kwargs = {'file_name': fname}
                
                if isinstance(class_tests, list):
                    # testing a function
                    kwargs['func_name'] = class_name
                    for case_data in class_tests:
                        yield self.create_testcase(case_data, **kwargs)
                        
                elif isinstance(class_tests, dict):
                    # testing a class
                    kwargs['class_name'] = class_name
                    for method_name, method_tests in class_tests.items():
                        kwargs['func_name'] = method_name
                        for case_data in method_tests:
                            yield self.create_testcase(case_data, **kwargs)
    
    def parse_yaml(self, fname):
        return load(open(fname), Loader=Loader)


class YamlTests(Plugin):
    """Run unittests specified in YAML files (.yml)
    """
    
    name = 'yamltests'
    yaml_test_parser = YamlTestParser()

    def options(self, parser, env=os.environ):
        super(YamlTests, self).options(parser, env=env)

    def configure(self, options, conf):
        #print >> sys.stderr, ("Conf: %s" % conf)
        super(YamlTests, self).configure(options, conf)
        if not self.enabled:
            return

    def finalize(self, result):
        pass

    def wantFile(self, fname):
        if fname.endswith('.yml'):
            return True
        return None

    def loadTestsFromFile(self, fname):
        """Return iterable containing TestCases
        """
        name = os.path.abspath(fname)
        flag = False
        for case in self.yaml_test_parser.get_cases(name):
            flag = True
            yield case
        if not flag:
            yield False

"""
if __name__ == "__main__":
     
     ytp = YamlTestParser()
     fh = open('tests.yml')
     print '='*80
     for case in ytp.get_cases(fh):
      test_result = unittest.TestResult()
      case.run(test_result)
      print 'Description:', case.description
      print 'Input:', case.input
      print 'Expected:', case.expected
      print 'Actual:', case.actual
      print 'Test result:', test_result
      for error in test_result.errors:
           print '\tError:', error[1]
      for failure in test_result.failures:
           print '\tFailure:', failure[1]
      print '-'*80
     print '='*80
"""