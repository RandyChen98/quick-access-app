import os
import sys
import threading
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item
import keyboard
import tkinter as tk

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.card_manager import CardManager
from core.clipboard_reader import ClipboardReader
from core.browser_launcher import BrowserLauncher
from ui.window import MainWindow


class QuickAccessApp:
    def __init__(self):
        self.card_manager = CardManager()
        self.clipboard_reader = ClipboardReader()
        self.browser_launcher = BrowserLauncher(self.clipboard_reader)
        
        self.main_window = None
        self.tray_icon = None
        self.hotkeys_registered = False
        
        self.setup_tray_icon()
        self.setup_hotkeys()
    
    def create_tray_image(self):
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        draw.rectangle([width//4, height//4, 3*width//4, 3*height//4], 
                      fill='blue', outline='darkblue')
        draw.text((width//2-8, height//2-8), "QA", fill='white')
        
        return image
    
    def setup_tray_icon(self):
        image = self.create_tray_image()
        
        menu = pystray.Menu(
            item('Open', self.show_window),
            item('Add Card', self.add_card_from_tray),
            pystray.Menu.SEPARATOR,
            item('Exit', self.quit_app)
        )
        
        self.tray_icon = pystray.Icon("QuickAccess", image, "Quick Access App", menu, default_action=self.show_window)
    
    def setup_hotkeys(self):
        if self.hotkeys_registered:
            return
        
        try:
            cards = self.card_manager.get_all_cards()
            for card in cards:
                hotkey = card.get('hotkey', '').strip()
                if hotkey:
                    try:
                        keyboard.add_hotkey(hotkey, lambda c=card: self.launch_card_by_hotkey(c))
                    except Exception:
                        pass
            self.hotkeys_registered = True
        except Exception:
            pass
    
    def refresh_hotkeys(self):
        try:
            keyboard.clear_all_hotkeys()
            self.hotkeys_registered = False
            self.setup_hotkeys()
        except Exception:
            pass
    
    def launch_card_by_hotkey(self, card):
        def launch_in_background():
            self.browser_launcher.launch_card(card)
        threading.Thread(target=launch_in_background, daemon=True).start()
    
    def show_window(self, icon=None, item=None):
        def create_window():
            if not self.main_window:
                self.main_window = MainWindow(
                    self.card_manager, 
                    self.browser_launcher, 
                    self.clipboard_reader
                )
                self.main_window.set_on_close_callback(self.hide_window)
                self.main_window.set_on_card_changed_callback(self.refresh_hotkeys)
            
            self.main_window.show()
            self.main_window.refresh_cards()
            self.refresh_hotkeys()
        
        if hasattr(self, 'root') and self.root:
            self.root.after(0, create_window)
        else:
            create_window()
    
    def hide_window(self):
        if self.main_window:
            self.main_window.hide()
    
    def add_card_from_tray(self, icon=None, item=None):
        self.show_window()
        if self.main_window:
            self.main_window.root.after(100, self.main_window.add_card)
    
    def quit_app(self, icon=None, item=None):
        if self.main_window:
            self.main_window.root.quit()
        
        try:
            keyboard.clear_all_hotkeys()
        except Exception:
            pass
        
        if self.clipboard_reader:
            self.clipboard_reader.stop_monitoring()
        
        if self.tray_icon:
            self.tray_icon.stop()
        
        os._exit(0)
    
    def run(self):
        self.clipboard_reader.start_monitoring()
        
        if self.tray_icon:
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
        
        self.root = tk.Tk()
        self.root.withdraw()
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.quit_app()


def main():
    app = QuickAccessApp()
    app.run()


if __name__ == "__main__":
    main()