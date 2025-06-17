# File Organizer GUI

A simple Python app to organize files into folders by type, with a user-friendly GUI.

## Features

- Select a folder to organize
- Customizable file type rules via `config.json`
- Logs all actions to `log.txt`
- Error handling and confirmations
- Edit config from the GUI

## Setup

1. **Install Python 3**  
   Download from [python.org](https://www.python.org/).

2. **Clone this repository**  
   ```sh
   git clone https://github.com/JRoetscyber/file-organizer-gui.git
   cd file-organizer-gui
   ```

3. **Install requirements**  
   No extra packages needed (uses built-in Tkinter).

4. **Run the app**  
   ```sh
   python main.py
   ```

## Usage

1. Click **Pick Folder** and select the folder you want to organize.
2. (Optional) Click **Edit Config** to customize file type rules.
3. Click **Start Organizing**. Confirm when prompted.
4. Check the log window or `log.txt` for details.

## Configuring File Types

Edit `config.json` to define which extensions go in which folders.  
Example:
```json
{
  "Documents": [".pdf", ".docx", ".txt"],
  "Images": [".jpg", ".png"],
  "Audio": [".mp3", ".wav"]
}
```
Unmatched files go to the `Others` folder.

## License

MIT License
