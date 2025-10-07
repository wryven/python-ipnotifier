import requests
import time

from pathlib import Path
from config_manager import ConfigManager

class Notifier:
    '''Handles checking the public IP and sending updates to Discord.'''

    # Public

    def __init__(self, config: ConfigManager) -> None:
        self.config = config
        self.__last_ip : str | None = None
    
    def run(self) -> None:
        """Start the notifier."""

        try:
            # Fetch current IP at startup
            startup_ip = self.__get_public_ip() or "unknown"
            self.__send_startup_message(startup_ip)
            self.__last_ip = startup_ip
            
            # Main loop
            while True: 
                current_ip = self.__get_public_ip()
                if current_ip: 
                    if current_ip != self.__last_ip:
                        self.__send_update_message(current_ip)
                        self.__last_ip = current_ip
                    else:
                        print(f"[=] Your IP has not changed.")
                else:
                    print(f"[!] Could not retrieve IP.")
                time.sleep(self.config.check_interval)
        except KeyboardInterrupt:
            self.__send_shutdown_message()
            print("[x] Notifier stopped by user.")                

    # Private
    
    def __get_public_ip(self) -> str | None:
        try:
            r = requests.get("https://api.ipify.org?format=json", timeout=5)
            r.raise_for_status()
            return r.json().get("ip")
        except Exception as e:
            print(f"[!] Error fetching IP: {e}")
            return None
        
    def __send_startup_message(self, ip) -> None:
        embed = {
            "title": "Notifier Started.",
            "description": f"The notifier has started, check interval is {self.config.check_interval} seconds. The current IP is {ip}.",
            "color": 0x00ff00
        }

        payload = {"embeds": [embed]}
        self.__send_to_discord(payload)



    def __send_update_message(self, ip) -> None:
        embed = {
            "title": "IP has changed.",
            "description": f"The new IP is {ip}.",
            "color": 0xffa500
        }     

        payload = {"embeds": [embed]}
        self.__send_to_discord(payload)           


    def __send_shutdown_message(self) -> None:
        embed = {
            "title": "Notifier stopped.",
            "description": "Notifier stopped by user.", #TODO: Posibility to stop by error maybe.
            "color": 0xff0000
        }

        payload = {"embeds": [embed]}
        self.__send_to_discord(payload)

    def __send_to_discord(self, payload) -> None:
        try: 
            r = requests.post(self.config.webhook_url, json=payload, timeout=5)
            r.raise_for_status()
            print(f"[✓] Sent message to Discord: {payload['embeds'][0]['title']}")
        except Exception as e:
            print(f"[!] Failed to send to Discord: {e}")
