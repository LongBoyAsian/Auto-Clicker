# Python Autoclicker

An autoclicker built with Python and Tkinter. It features a GUI that stays on top of other windows, click delay customization, and a global hotkey listener.

## Features

- **Global Hotkeys:** Start or pause the autoclicker from anywhere, even while in a game.
- **Customizable Speed:** Change the click delay in real-time directly from the UI.
- **Disable Mode:** Temporarily disable the hotkeys so you can type normally without accidentally triggering the clicker.
- **Always on Top:** The application window stays above other applications for easy monitoring and access.

## Default Keybinds

- **`s`** - Start / Pause the autoclicker.

## Requirements

- Python 3.x
- `pynput`

## How to Run Locally

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the script:
   ```bash
   python autoclicker.py
   ```

## How to Build the Standalone Executable (.exe)

You can compile this project into a standalone executable that does not require Python to run. 

Run the following command in the project directory using the provided PyInstaller spec file:
```bash
python -m PyInstaller autoclicker.spec
```
The compiled `.exe` will be located in the newly generated `dist/` directory.