# Quick Access App

A lightweight desktop application that runs in the system tray and allows users to quickly access predefined web addresses with dynamic parameter replacement functionality.

## Features

- **System Tray Operation**: Runs continuously in the background with a system tray icon
- **Card-based Interface**: Simple UI with clickable cards, each bound to a web address
- **Dynamic Parameter Replacement**: Support for `{content}` placeholder in URLs that gets replaced with selected text
- **Clipboard Integration**: Automatically captures selected text from other applications
- **Hotkey Support**: Configurable keyboard shortcuts for each card
- **Configuration Persistence**: Settings saved in JSON format
- **Cross-platform Support**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Packages

- `pystray`: System tray functionality
- `keyboard`: Global hotkey support
- `pyperclip`: Clipboard access
- `pillow`: Image processing for tray icon

## Usage

### Running the Application

```bash
python main.py
```

The application will start in the background with a system tray icon.

### Basic Operations

1. **Access Main Window**: Click the system tray icon and select "Open"
2. **Add Card**: Click "Add Card" button or use tray menu
3. **Edit Card**: Click "Edit Card" and select the card ID
4. **Delete Card**: Click "Delete Card" and select the card ID
5. **Launch Card**: Click any card to open its URL in the default browser

### Dynamic Parameter Replacement

Cards can contain the `{content}` placeholder in their URLs:

1. Create a card with URL like: `https://www.google.com/search?q={content}`
2. Select text in any application (VS Code, browser, etc.)
3. Click the card or use its hotkey
4. The selected text replaces `{content}` and opens in the browser

### Example Use Case

1. Create a card with:
   - Name: "GitHub Search"
   - URL: `https://github.com/search?q={content}`
   - Hotkey: `ctrl+shift+g`

2. Select code in VS Code
3. Press `Ctrl+Shift+G`
4. Browser opens with GitHub search for the selected code

### Hotkeys

- Hotkeys are global and work from any application
- Use standard key combinations like `ctrl+shift+g`
- Each card can have a unique hotkey
- Hotkeys are automatically registered when the main window opens

## Configuration

Settings are stored in `config/settings.json`:

```json
{
  "cards": [
    {
      "id": 1,
      "name": "Google Search",
      "url": "https://www.google.com/search?q={content}",
      "hotkey": "ctrl+shift+g"
    }
  ]
}
```

### Card Properties

- `id`: Unique identifier
- `name`: Display name for the card
- `url`: Target URL (can include `{content}` placeholder)
- `hotkey`: Optional keyboard shortcut

## Development

### Directory Structure

```
quick-access-app/
├── main.py                 # Application entry point
├── ui/
│   └── window.py           # Main window and UI logic
├── core/
│   ├── card_manager.py     # Card CRUD operations
│   ├── browser_launcher.py # URL launching with parameter replacement
│   └── clipboard_reader.py # Clipboard monitoring
├── config/
│   └── settings.json       # Configuration file
├── tests/
│   ├── test_card_manager.py
│   ├── test_browser_launcher.py
│   └── test_clipboard_reader.py
└── README.md
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test
python -m unittest tests.test_card_manager
```

### Code Style

- No comments in code (self-documenting)
- Type hints where beneficial
- Exception handling for robustness
- Modular design with clear separation of concerns

## Troubleshooting

### Common Issues

1. **Hotkeys not working**: 
   - Ensure the application has necessary permissions
   - Check if hotkey conflicts with other applications

2. **Clipboard not updating**:
   - Some applications may not update clipboard on text selection
   - Try copying text explicitly (Ctrl+C)

3. **Browser not opening**:
   - Ensure default browser is set
   - Check URL format (should include http:// or https://)

### Platform-specific Notes

- **Windows**: May require running as administrator for global hotkeys
- **macOS**: Requires accessibility permissions for clipboard monitoring
- **Linux**: Depends on desktop environment and clipboard manager

## License

This project is open source and available under the MIT License.