import time
import json
import logging
import os

# Import custom modules
from telegram_notifier import TelegramNotifier
from solar_api import SolarAPI

# Get directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load configuration from JSON
config_path = os.path.join(script_dir, "config.json")
with open(config_path, "r") as file:
    config = json.load(file)

# Load localization from JSON
localization_path = os.path.join(script_dir, "localization.json")
with open(localization_path, "r") as file:
    localization = json.load(file)

# Set language
LANGUAGE = config.get("language", "en")

def get_text(key):
    """Retrieve localized text based on the selected language."""
    return localization.get(LANGUAGE, {}).get(key, key)

# Initialize modules
SOLAR_API_IP = config["solar_api_ip"]
solar_api = SolarAPI(SOLAR_API_IP)
telegram = TelegramNotifier(config["telegram_token"], config["chat_id"])

# Convert minutes to seconds
CHECK_INTERVAL = config["check_interval_min"] * 60

# Get consecutive checks required from config, default to 1 if not specified
CONSECUTIVE_FULL_CHECKS = config.get("consecutive_full_checks", 1)
CONSECUTIVE_NOT_FULL_CHECKS = config.get("consecutive_not_full_checks", 1)

# Smart plug configuration (optional)
import smart_plug
SMART_PLUG_ENABLED = smart_plug.initialize_smart_plug(config)

# Variables to track battery state
battery_full_alert_sent = False
battery_not_full_alert_sent = False
consecutive_full_count = 0
consecutive_not_full_count = 0

# Set up logging
log_path = os.path.join(script_dir, "solar_monitor.log")
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_telegram_message(message):
    """Sends a message via Telegram Bot."""
    telegram.send_message(message)

def control_smart_plug(turn_on=False):
    """Controls the smart plug if enabled."""
    if not SMART_PLUG_ENABLED:
        return
    
    smart_plug.control_smart_plug(config, turn_on)

def fetch_solar_data():
    """Fetches real-time solar power data."""
    return solar_api.fetch_data()

def check_solar_data():
    """Checks battery status and sends alerts if needed."""
    global battery_full_alert_sent, battery_not_full_alert_sent
    global consecutive_full_count, consecutive_not_full_count
    data = fetch_solar_data()

    if not data:
        return

    try:
        battery_mode, battery_soc, battery_is_full = solar_api.get_battery_status(data)

        if battery_is_full:
            consecutive_full_count += 1
            consecutive_not_full_count = 0
        else:
            consecutive_not_full_count += 1
            consecutive_full_count = 0

        if consecutive_full_count >= CONSECUTIVE_FULL_CHECKS and not battery_full_alert_sent:
            send_telegram_message(f"{get_text('battery_full')} ({battery_soc}%)")
            battery_full_alert_sent = True
            battery_not_full_alert_sent = False
            # Turn on smart plug when battery is full
            control_smart_plug(turn_on=True)
        elif consecutive_not_full_count >= CONSECUTIVE_NOT_FULL_CHECKS and not battery_not_full_alert_sent:
            send_telegram_message(f"{get_text('battery_not_full')} ({battery_soc}%)")
            battery_not_full_alert_sent = True
            battery_full_alert_sent = False
            # Turn off smart plug when battery is not full
            control_smart_plug(turn_on=False)

    except KeyError as e:
        logging.error(f"Missing data field: {e}")

if __name__ == "__main__":
    logging.info(get_text("bot_start"))
    send_telegram_message(get_text("bot_start"))
    
    # Immediate first check
    data = fetch_solar_data()
    if data:
        try:
            battery_mode, battery_soc, battery_is_full = solar_api.get_battery_status(data)
            
            if battery_is_full:
                send_telegram_message(f"{get_text('battery_full')} ({battery_soc}%)")
                battery_full_alert_sent = True
                battery_not_full_alert_sent = False
                # Turn on smart plug when battery is full
                control_smart_plug(turn_on=True)
            else:
                send_telegram_message(f"{get_text('battery_not_full')} ({battery_soc}%)")
                battery_not_full_alert_sent = True
                battery_full_alert_sent = False
                # Turn off smart plug when battery is not full
                control_smart_plug(turn_on=False)
        except KeyError as e:
            logging.error(f"Missing data field on startup: {e}")
    
    while True:
        check_solar_data()
        time.sleep(CHECK_INTERVAL)
