import platform
import os
from selenium.webdriver.chrome.service import Service

class WebDriverService:
    def __init__(self):
        # Determine the operating system
        self.system = platform.system()
        self.architecture = platform.machine()
        # Define the paths to driver executables
        self.driver_paths = {
            "Windows": "selenium-versions/chromedriver-win64/chromedriver.exe",
            "macOS": "selenium-versions/chromedriver-mac-x64",
            "macOS ARM": "selenium-versions/chromedriver-mac-arm64",
        }
    def get_driver_path(self):
        # Return the correct driver path based on the OS and architecture
        if self.system == "Windows":
            return self.driver_paths["Windows"]
        elif self.system == "Darwin":  # macOS
            if self.architecture == "arm64":
                return self.driver_paths["macOS ARM"]
            else:
                return self.driver_paths["macOS"]
        else:
            raise OSError("Unsupported operating system")
    def get_service(self):
        # Initialize the Service class with the correct executable path
        driver_path = self.get_driver_path()
        print(os.path.exists(driver_path))
        if not os.path.exists(driver_path):
            raise FileNotFoundError(f"Driver executable not found: {driver_path}")
        return Service(driver_path)