import unittest
from example.extractor import extract, Extractor

class TestExtractFunction(unittest.TestCase):
    
    def test_extract(self):
        msg = "Extract mention at the begining of a tweet"
        text = "@username reply"
        expected = "username"
        actual = extract(text)
        self.assertEqual(actual, expected)
    
class TestExtractorClass(unittest.TestCase):
    
    def setUp(self):
        self.ex = Extractor()
    
    def test_extract(self):
        msg = "Extract mention at the begining of a tweet"
        text = "@username reply"
        expected = ["username"]
        actual = self.ex.extract(text)
        self.assertEqual(actual, expected)
