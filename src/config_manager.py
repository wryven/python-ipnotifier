import json
import sys

from pathlib import Path

class ConfigManager:
    ''' Handles loading and providing access to configurations.'''

    # Config keys
    KEY_WEBHOOK_URL = "webhook_url"
    KEY_CHECK_INTERVAL = "check_interval"

    # Default values
    DEFAULT_CHECK_INTERVAL = 300

    # Methods
    def __init__(self, path: str = "config/config.json"):

        #Detect if running in PyInstaller
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).parent.parent  # Because we are on src we go back twice.

        self.path = Path(path)
        self._data = {}
        self.load()

    def load(self):
        try: 
            with self.path.open("r") as file:
                self._data = json.load(file)

            if not self._data.get(self.KEY_WEBHOOK_URL):
                raise ValueError(f"{self.KEY_WEBHOOK_URL} key is missing or empty in config file.")

            self._data.setdefault(self.KEY_CHECK_INTERVAL, self.DEFAULT_CHECK_INTERVAL)
        
        except Exception as e: 
            print(f"[!] failed to load config file: {e}")
            sys.exit(1)

    # Properties
    @property
    def webhook_url(self) -> str:
        return self._data[self.KEY_WEBHOOK_URL]
    
    @property
    def check_interval(self) -> int:
        return self._data[self.KEY_CHECK_INTERVAL]