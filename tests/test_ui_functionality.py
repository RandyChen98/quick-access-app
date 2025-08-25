import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.card_manager import CardManager


class TestUIFunctionality(unittest.TestCase):
    def setUp(self):
        self.card_manager = CardManager(config_path="/tmp/test_settings.json")
        
        self.test_card = self.card_manager.add_card(
            "Test Card", 
            "https://example.com/{content}", 
            "ctrl+t"
        )
    
    def tearDown(self):
        import os
        try:
            os.remove("/tmp/test_settings.json")
        except FileNotFoundError:
            pass
    
    def test_individual_card_edit_functionality(self):
        card = self.card_manager.get_card(self.test_card)
        self.assertIsNotNone(card)
        self.assertEqual(card['name'], "Test Card")
        
        updated = self.card_manager.update_card(
            self.test_card, 
            "Updated Card", 
            "https://updated.com/{content}", 
            "ctrl+u"
        )
        self.assertTrue(updated)
        
        updated_card = self.card_manager.get_card(self.test_card)
        self.assertEqual(updated_card['name'], "Updated Card")
        self.assertEqual(updated_card['url'], "https://updated.com/{content}")
        self.assertEqual(updated_card['hotkey'], "ctrl+u")
    
    def test_card_delete_functionality(self):
        card_count_before = len(self.card_manager.get_all_cards())
        
        deleted = self.card_manager.delete_card(self.test_card)
        self.assertTrue(deleted)
        
        card_count_after = len(self.card_manager.get_all_cards())
        self.assertEqual(card_count_after, card_count_before - 1)
        
        card = self.card_manager.get_card(self.test_card)
        self.assertIsNone(card)


if __name__ == '__main__':
    unittest.main()