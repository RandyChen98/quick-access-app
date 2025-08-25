import unittest
import tempfile
import os
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.card_manager import CardManager


class TestCardManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_settings.json")
        self.card_manager = CardManager(self.config_path)
    
    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)
    
    def test_add_card(self):
        card_id = self.card_manager.add_card("Test Card", "https://example.com", "ctrl+t")
        self.assertEqual(card_id, 1)
        
        cards = self.card_manager.get_all_cards()
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]['name'], "Test Card")
        self.assertEqual(cards[0]['url'], "https://example.com")
        self.assertEqual(cards[0]['hotkey'], "ctrl+t")
    
    def test_update_card(self):
        card_id = self.card_manager.add_card("Original", "https://original.com", "")
        
        success = self.card_manager.update_card(card_id, name="Updated", url="https://updated.com")
        self.assertTrue(success)
        
        card = self.card_manager.get_card(card_id)
        self.assertEqual(card['name'], "Updated")
        self.assertEqual(card['url'], "https://updated.com")
    
    def test_delete_card(self):
        card_id = self.card_manager.add_card("To Delete", "https://example.com")
        
        success = self.card_manager.delete_card(card_id)
        self.assertTrue(success)
        
        card = self.card_manager.get_card(card_id)
        self.assertIsNone(card)
    
    def test_get_card_by_hotkey(self):
        self.card_manager.add_card("Card 1", "https://example1.com", "ctrl+1")
        self.card_manager.add_card("Card 2", "https://example2.com", "ctrl+2")
        
        card = self.card_manager.get_card_by_hotkey("ctrl+1")
        self.assertIsNotNone(card)
        self.assertEqual(card['name'], "Card 1")
        
        card = self.card_manager.get_card_by_hotkey("ctrl+3")
        self.assertIsNone(card)
    
    def test_persistence(self):
        self.card_manager.add_card("Persistent Card", "https://persist.com", "ctrl+p")
        
        new_manager = CardManager(self.config_path)
        cards = new_manager.get_all_cards()
        
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]['name'], "Persistent Card")


if __name__ == '__main__':
    unittest.main()