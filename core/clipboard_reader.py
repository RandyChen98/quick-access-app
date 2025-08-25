import pyperclip
import threading
import time


class ClipboardReader:
    def __init__(self):
        self.last_clipboard_content = ""
        self.selected_content = ""
        self.monitoring = False
        self.monitor_thread = None
    
    def get_clipboard_content(self) -> str:
        try:
            content = pyperclip.paste()
            return content if content else ""
        except Exception:
            return ""
    
    def get_selected_content(self) -> str:
        current_clipboard = self.get_clipboard_content()
        if current_clipboard != self.last_clipboard_content:
            self.selected_content = current_clipboard
            self.last_clipboard_content = current_clipboard
        return self.selected_content
    
    def start_monitoring(self):
        if not self.monitoring:
            self.monitoring = True
            self.last_clipboard_content = self.get_clipboard_content()
            self.monitor_thread = threading.Thread(target=self._monitor_clipboard, daemon=True)
            self.monitor_thread.start()
    
    def stop_monitoring(self):
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
    
    def _monitor_clipboard(self):
        while self.monitoring:
            try:
                current_content = self.get_clipboard_content()
                if current_content != self.last_clipboard_content:
                    self.selected_content = current_content
                    self.last_clipboard_content = current_content
                time.sleep(0.1)
            except Exception:
                pass
    
    def clear_selected_content(self):
        self.selected_content = ""