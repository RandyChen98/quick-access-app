import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Callable, Optional
import threading


class CardDialog:
    def __init__(self, parent, title: str, name: str = "", url: str = "", hotkey: str = ""):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.dialog.geometry(f"+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        
        frame = ttk.Frame(self.dialog, padding="10")
        frame.grid(row=0, column=0, sticky="ew")
        
        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w", pady=2)
        self.name_entry = ttk.Entry(frame, width=40)
        self.name_entry.grid(row=0, column=1, pady=2)
        self.name_entry.insert(0, name)
        
        ttk.Label(frame, text="URL:").grid(row=1, column=0, sticky="w", pady=2)
        self.url_entry = ttk.Entry(frame, width=40)
        self.url_entry.grid(row=1, column=1, pady=2)
        self.url_entry.insert(0, url)
        
        ttk.Label(frame, text="Hotkey:").grid(row=2, column=0, sticky="w", pady=2)
        self.hotkey_entry = ttk.Entry(frame, width=40)
        self.hotkey_entry.grid(row=2, column=1, pady=2)
        self.hotkey_entry.insert(0, hotkey)
        
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
        
        self.name_entry.focus()
        self.dialog.bind('<Return>', lambda e: self.ok_clicked())
        self.dialog.bind('<Escape>', lambda e: self.cancel_clicked())
    
    def ok_clicked(self):
        name = self.name_entry.get().strip()
        url = self.url_entry.get().strip()
        hotkey = self.hotkey_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Name is required")
            return
        if not url:
            messagebox.showerror("Error", "URL is required")
            return
        
        self.result = (name, url, hotkey)
        self.dialog.destroy()
    
    def cancel_clicked(self):
        self.dialog.destroy()


class MainWindow:
    def __init__(self, card_manager, browser_launcher, clipboard_reader):
        self.card_manager = card_manager
        self.browser_launcher = browser_launcher
        self.clipboard_reader = clipboard_reader
        self.on_close_callback = None
        
        self.root = tk.Tk()
        self.root.title("Quick Access App")
        self.root.geometry("600x400")
        
        self.setup_ui()
        self.refresh_cards()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        toolbar = ttk.Frame(main_frame)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Button(toolbar, text="Add Card", command=self.add_card).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Edit Card", command=self.edit_card).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Delete Card", command=self.delete_card).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Refresh", command=self.refresh_cards).pack(side=tk.LEFT, padx=5)
        
        self.cards_frame = ttk.Frame(main_frame)
        self.cards_frame.grid(row=1, column=0, sticky="nsew")
        
        canvas = tk.Canvas(self.cards_frame, bg="white")
        scrollbar = ttk.Scrollbar(self.cards_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.cards_frame.grid_rowconfigure(0, weight=1)
        self.cards_frame.grid_columnconfigure(0, weight=1)
    
    def refresh_cards(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        cards = self.card_manager.get_all_cards()
        for i, card in enumerate(cards):
            self.create_card_widget(card, i)
    
    def create_card_widget(self, card, row):
        card_frame = ttk.Frame(self.scrollable_frame, relief="raised", borderwidth=1)
        card_frame.grid(row=row, column=0, sticky="ew", pady=2, padx=5)
        card_frame.grid_columnconfigure(0, weight=1)
        
        name_label = ttk.Label(card_frame, text=card['name'], font=('Arial', 12, 'bold'))
        name_label.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))
        
        url_label = ttk.Label(card_frame, text=card['url'], foreground="blue")
        url_label.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 2))
        
        if card.get('hotkey'):
            hotkey_label = ttk.Label(card_frame, text=f"Hotkey: {card['hotkey']}", 
                                   font=('Arial', 9), foreground="gray")
            hotkey_label.grid(row=2, column=0, sticky="w", padx=10, pady=(0, 5))
        
        button_frame = ttk.Frame(card_frame)
        button_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=5)
        
        launch_button = ttk.Button(button_frame, text="Launch", 
                                 command=lambda c=card: self.launch_card(c))
        launch_button.pack(side=tk.TOP, pady=1)
        
        edit_button = ttk.Button(button_frame, text="Edit", 
                               command=lambda c=card: self.edit_specific_card(c))
        edit_button.pack(side=tk.TOP, pady=1)
        
        card_frame.bind("<Button-1>", lambda e, c=card: self.launch_card(c))
        card_frame.bind("<Button-3>", lambda e, c=card: self.show_card_context_menu(e, c))
        name_label.bind("<Button-1>", lambda e, c=card: self.launch_card(c))
        name_label.bind("<Button-3>", lambda e, c=card: self.show_card_context_menu(e, c))
        url_label.bind("<Button-1>", lambda e, c=card: self.launch_card(c))
        url_label.bind("<Button-3>", lambda e, c=card: self.show_card_context_menu(e, c))
    
    def launch_card(self, card):
        def launch_async():
            success = self.browser_launcher.launch_card(card)
            if not success:
                self.root.after(0, lambda: messagebox.showerror("Error", "Failed to launch browser"))
        
        threading.Thread(target=launch_async, daemon=True).start()
    
    def add_card(self):
        dialog = CardDialog(self.root, "Add Card")
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            name, url, hotkey = dialog.result
            self.card_manager.add_card(name, url, hotkey)
            self.refresh_cards()
    
    def edit_card(self):
        cards = self.card_manager.get_all_cards()
        if not cards:
            messagebox.showinfo("Info", "No cards to edit")
            return
        
        card_names = [f"{card['id']}: {card['name']}" for card in cards]
        selection = simpledialog.askstring("Select Card", 
                                         f"Enter card ID to edit:\n" + "\n".join(card_names))
        
        if selection:
            try:
                card_id = int(selection.split(':')[0])
                card = self.card_manager.get_card(card_id)
                if card:
                    dialog = CardDialog(self.root, "Edit Card", 
                                      card['name'], card['url'], card.get('hotkey', ''))
                    self.root.wait_window(dialog.dialog)
                    
                    if dialog.result:
                        name, url, hotkey = dialog.result
                        self.card_manager.update_card(card_id, name, url, hotkey)
                        self.refresh_cards()
                else:
                    messagebox.showerror("Error", "Card not found")
            except ValueError:
                messagebox.showerror("Error", "Invalid card ID")
    
    def edit_specific_card(self, card):
        dialog = CardDialog(self.root, "Edit Card", 
                          card['name'], card['url'], card.get('hotkey', ''))
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            name, url, hotkey = dialog.result
            self.card_manager.update_card(card['id'], name, url, hotkey)
            self.refresh_cards()
    
    def show_card_context_menu(self, event, card):
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Launch", command=lambda: self.launch_card(card))
        context_menu.add_command(label="Edit", command=lambda: self.edit_specific_card(card))
        context_menu.add_command(label="Delete", command=lambda: self.delete_specific_card(card))
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def delete_specific_card(self, card):
        if messagebox.askyesno("Confirm", f"Delete card '{card['name']}'?"):
            if self.card_manager.delete_card(card['id']):
                self.refresh_cards()
            else:
                messagebox.showerror("Error", "Card not found")
    
    def delete_card(self):
        cards = self.card_manager.get_all_cards()
        if not cards:
            messagebox.showinfo("Info", "No cards to delete")
            return
        
        card_names = [f"{card['id']}: {card['name']}" for card in cards]
        selection = simpledialog.askstring("Select Card", 
                                         f"Enter card ID to delete:\n" + "\n".join(card_names))
        
        if selection:
            try:
                card_id = int(selection.split(':')[0])
                if messagebox.askyesno("Confirm", f"Delete card {card_id}?"):
                    if self.card_manager.delete_card(card_id):
                        self.refresh_cards()
                    else:
                        messagebox.showerror("Error", "Card not found")
            except ValueError:
                messagebox.showerror("Error", "Invalid card ID")
    
    def set_on_close_callback(self, callback: Callable):
        self.on_close_callback = callback
    
    def on_window_close(self):
        if self.on_close_callback:
            self.on_close_callback()
        else:
            self.root.withdraw()
    
    def show(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def hide(self):
        self.root.withdraw()
    
    def run(self):
        self.root.mainloop()