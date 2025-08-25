import json
import os
from typing import List, Dict, Any


class CardManager:
    def __init__(self, config_path: str = "config/settings.json"):
        self.config_path = config_path
        self.cards = []
        self.load_cards()
    
    def load_cards(self):
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cards = data.get('cards', [])
            else:
                self.cards = []
                self.save_cards()
        except Exception:
            self.cards = []
    
    def save_cards(self):
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            data = {'cards': self.cards}
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def add_card(self, name: str, url: str, hotkey: str = "") -> int:
        card_id = len(self.cards) + 1
        card = {
            'id': card_id,
            'name': name,
            'url': url,
            'hotkey': hotkey
        }
        self.cards.append(card)
        self.save_cards()
        return card_id
    
    def update_card(self, card_id: int, name: str = None, url: str = None, hotkey: str = None) -> bool:
        for card in self.cards:
            if card['id'] == card_id:
                if name is not None:
                    card['name'] = name
                if url is not None:
                    card['url'] = url
                if hotkey is not None:
                    card['hotkey'] = hotkey
                self.save_cards()
                return True
        return False
    
    def delete_card(self, card_id: int) -> bool:
        for i, card in enumerate(self.cards):
            if card['id'] == card_id:
                del self.cards[i]
                self.save_cards()
                return True
        return False
    
    def get_card(self, card_id: int) -> Dict[str, Any]:
        for card in self.cards:
            if card['id'] == card_id:
                return card.copy()
        return None
    
    def get_all_cards(self) -> List[Dict[str, Any]]:
        return [card.copy() for card in self.cards]
    
    def get_card_by_hotkey(self, hotkey: str) -> Dict[str, Any]:
        for card in self.cards:
            if card.get('hotkey') == hotkey:
                return card.copy()
        return None