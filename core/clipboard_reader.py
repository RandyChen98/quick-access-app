import pyperclip
import threading
import time
import platform
import subprocess


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
        selected_text = self.try_get_selected_text()
        if selected_text:
            self.selected_content = selected_text
            return selected_text
        
        current_clipboard = self.get_clipboard_content()
        if current_clipboard != self.last_clipboard_content:
            self.selected_content = current_clipboard
            self.last_clipboard_content = current_clipboard
        return self.selected_content
    
    def try_get_selected_text(self) -> str:
        try:
            system = platform.system().lower()
            
            if system == "linux":
                try:
                    result = subprocess.run(['xsel', '-o'], capture_output=True, text=True, timeout=1)
                    if result.returncode == 0 and result.stdout.strip():
                        return result.stdout.strip()
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
                
                try:
                    result = subprocess.run(['xclip', '-o'], capture_output=True, text=True, timeout=1)
                    if result.returncode == 0 and result.stdout.strip():
                        return result.stdout.strip()
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
            
            elif system == "darwin":
                try:
                    result = subprocess.run(['pbpaste'], capture_output=True, text=True, timeout=1)
                    if result.returncode == 0 and result.stdout.strip():
                        clipboard_content = result.stdout.strip()
                        if clipboard_content != self.last_clipboard_content:
                            return clipboard_content
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
            
            elif system == "windows":
                try:
                    import win32clipboard
                    import win32con
                    win32clipboard.OpenClipboard()
                    data = win32clipboard.GetClipboardData(win32con.CF_TEXT)
                    win32clipboard.CloseClipboard()
                    if data and data.strip() != self.last_clipboard_content:
                        return data.strip()
                except ImportError:
                    pass
                except Exception:
                    pass
            
        except Exception:
            pass
        
        return ""
    
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