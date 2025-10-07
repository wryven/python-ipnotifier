import sys
from config_manager import ConfigManager
from notifier import Notifier


def main():
    config = ConfigManager()
    notifier = Notifier(config)

    notifier.run()


if __name__ == "__main__":
    main()
