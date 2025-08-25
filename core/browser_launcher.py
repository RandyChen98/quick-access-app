import webbrowser
import urllib.parse
from typing import Dict, Any


class BrowserLauncher:
    def __init__(self, clipboard_reader=None):
        self.clipboard_reader = clipboard_reader
    
    def replace_parameters(self, url: str, content: str = None) -> str:
        if content is None and self.clipboard_reader:
            content = self.clipboard_reader.get_selected_content()
        
        if content:
            encoded_content = urllib.parse.quote(content, safe='')
            url = url.replace('{content}', encoded_content)
        else:
            url = url.replace('{content}', '')
        
        return url
    
    def launch_url(self, url: str, content: str = None) -> bool:
        try:
            final_url = self.replace_parameters(url, content)
            if not final_url.startswith(('http://', 'https://')):
                if '://' not in final_url:
                    final_url = 'https://' + final_url
            webbrowser.open(final_url)
            return True
        except Exception:
            return False
    
    def launch_card(self, card: Dict[str, Any], content: str = None) -> bool:
        if not card or 'url' not in card:
            return False
        return self.launch_url(card['url'], content)