import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.browser_launcher import BrowserLauncher


class MockClipboardReader:
    def __init__(self, content="test content"):
        self.content = content
    
    def get_selected_content(self):
        return self.content


class TestBrowserLauncher(unittest.TestCase):
    def setUp(self):
        self.clipboard_reader = MockClipboardReader()
        self.browser_launcher = BrowserLauncher(self.clipboard_reader)
    
    def test_replace_parameters_with_content(self):
        url = "https://google.com/search?q={content}"
        result = self.browser_launcher.replace_parameters(url, "python")
        self.assertEqual(result, "https://google.com/search?q=python")
    
    def test_replace_parameters_with_clipboard(self):
        url = "https://google.com/search?q={content}"
        result = self.browser_launcher.replace_parameters(url)
        self.assertEqual(result, "https://google.com/search?q=test%20content")
    
    def test_replace_parameters_empty_content(self):
        url = "https://google.com/search?q={content}"
        result = self.browser_launcher.replace_parameters(url, "")
        self.assertEqual(result, "https://google.com/search?q=")
    
    def test_replace_parameters_no_placeholder(self):
        url = "https://google.com"
        result = self.browser_launcher.replace_parameters(url, "test")
        self.assertEqual(result, "https://google.com")
    
    def test_replace_parameters_special_characters(self):
        url = "https://google.com/search?q={content}"
        content = "hello world & test"
        result = self.browser_launcher.replace_parameters(url, content)
        self.assertEqual(result, "https://google.com/search?q=hello%20world%20%26%20test")
    
    def test_launch_card_valid(self):
        card = {
            'name': 'Test Card',
            'url': 'https://google.com/search?q={content}',
            'hotkey': 'ctrl+t'
        }
        
        result = self.browser_launcher.launch_card(card, "test query")
        self.assertTrue(result)
    
    def test_launch_card_invalid(self):
        card = None
        result = self.browser_launcher.launch_card(card)
        self.assertFalse(result)
        
        card = {'name': 'Invalid'}
        result = self.browser_launcher.launch_card(card)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()