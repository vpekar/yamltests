import os
import unittest
from nose.plugins import PluginTester
from yamltests import YamlTests

class TestRunsPythonTests(PluginTester, unittest.TestCase):
    """Make sure python tests run as expected, with yamltests enabled
    """

    activate = "--with-yamltests"
    plugins = [YamlTests()]
    suitepath = os.path.join(os.getcwd(), 'example/tests/tests.py')
    
    def test_run_python_tests(self):
        assert "FAILED" not in self.output

class TestRunsYAMLTests(PluginTester, unittest.TestCase):
    """Make sure YAML tests run as expected
    """

    activate = "--with-yamltests"
    plugins = [YamlTests()]
    suitepath = os.path.join(os.getcwd(), 'example/tests/tests.yml')
    
    def test_run_yaml_tests(self):
        assert "FAILED" not in self.output


if __name__ == '__main__':
    unittest.main()
    