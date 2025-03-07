import time
import json
import logging
import os
import sys

# Set up logging to console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Get directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load configuration from JSON
config_path = os.path.join(script_dir, "config.json")
try:
    with open(config_path, "r") as file:
        config = json.load(file)
except FileNotFoundError:
    logging.error(f"Config file not found at {config_path}")
    logging.error("Please rename _config.json to config.json and configure it")
    sys.exit(1)
except json.JSONDecodeError:
    logging.error(f"Invalid JSON in config file at {config_path}")
    sys.exit(1)

# Import smart plug module
from modules import smart_plug

def test_smart_plug_toggle():
    """Test function to toggle smart plug on and off every 7 seconds"""
    
    # Check if smart plug is enabled in config
    if "smart_plug" not in config or not config["smart_plug"].get("enabled", False):
        logging.error("Smart plug is not enabled in config.json")
        logging.error("Please set 'enabled' to true in the 'smart_plug' section")
        return False
    
    # Initialize smart plug
    if not smart_plug.initialize_smart_plug(config):
        logging.error("Failed to initialize smart plug")
        return False
    
    logging.info("Starting smart plug toggle test (Ctrl+C to exit)")
    logging.info("Will toggle smart plug ON and OFF every 5 seconds")
    
    toggle_state = False
    try:
        while True:
            toggle_state = not toggle_state
            logging.info(f"Setting smart plug to {'ON' if toggle_state else 'OFF'}")
            smart_plug.control_smart_plug(config, toggle_state)
            time.sleep(5)
    except KeyboardInterrupt:
        logging.info("Test stopped by user")
        return True
    except Exception as e:
        logging.error(f"Error during test: {e}")
        return False

if __name__ == "__main__":
    test_smart_plug_toggle()