import unittest
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.clipboard_reader import ClipboardReader


class TestClipboardReader(unittest.TestCase):
    def setUp(self):
        self.clipboard_reader = ClipboardReader()
    
    def tearDown(self):
        self.clipboard_reader.stop_monitoring()
    
    def test_get_clipboard_content(self):
        content = self.clipboard_reader.get_clipboard_content()
        self.assertIsInstance(content, str)
    
    def test_get_selected_content_initial(self):
        content = self.clipboard_reader.get_selected_content()
        self.assertIsInstance(content, str)
    
    def test_clear_selected_content(self):
        self.clipboard_reader.selected_content = "test"
        self.clipboard_reader.clear_selected_content()
        self.assertEqual(self.clipboard_reader.selected_content, "")
    
    def test_monitoring_start_stop(self):
        self.assertFalse(self.clipboard_reader.monitoring)
        
        self.clipboard_reader.start_monitoring()
        self.assertTrue(self.clipboard_reader.monitoring)
        
        self.clipboard_reader.stop_monitoring()
        self.assertFalse(self.clipboard_reader.monitoring)
    
    def test_monitoring_multiple_starts(self):
        self.clipboard_reader.start_monitoring()
        first_thread = self.clipboard_reader.monitor_thread
        
        self.clipboard_reader.start_monitoring()
        second_thread = self.clipboard_reader.monitor_thread
        
        self.assertEqual(first_thread, second_thread)
        self.assertTrue(self.clipboard_reader.monitoring)


if __name__ == '__main__':
    unittest.main()