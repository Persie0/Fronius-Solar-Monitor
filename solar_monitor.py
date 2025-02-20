import time
import json
import requests
import logging
import os

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

# Telegram Bot details
TELEGRAM_TOKEN = config["telegram_token"]
CHAT_ID = config["chat_id"]

# Hardcoded API path with dynamic IP
SOLAR_API_IP = config["solar_api_ip"]
API_URL = f"http://{SOLAR_API_IP}/solar_api/v1/GetPowerFlowRealtimeData.fcgi"

# Convert minutes to seconds
CHECK_INTERVAL = config["check_interval_min"] * 60

# Get consecutive checks required from config, default to 1 if not specified
CONSECUTIVE_FULL_CHECKS = config.get("consecutive_full_checks", 1)
CONSECUTIVE_NOT_FULL_CHECKS = config.get("consecutive_not_full_checks", 1)

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
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logging.info("Telegram message sent successfully: %s", message)
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send Telegram message: {e}")

def fetch_solar_data():
    """Fetches real-time solar power data."""
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching solar data: {e}")
        return None

def check_solar_data():
    """Checks battery status and sends alerts if needed."""
    global battery_full_alert_sent, battery_not_full_alert_sent
    global consecutive_full_count, consecutive_not_full_count
    data = fetch_solar_data()

    if not data:
        return

    try:
        battery_mode = data["Body"]["Data"]["Inverters"]["1"].get("Battery_Mode", "")
        battery_is_full = battery_mode == "battery full"

        if battery_is_full:
            consecutive_full_count += 1
            consecutive_not_full_count = 0
        else:
            consecutive_not_full_count += 1
            consecutive_full_count = 0

        if consecutive_full_count >= CONSECUTIVE_FULL_CHECKS and not battery_full_alert_sent:
            send_telegram_message(get_text("battery_full"))
            battery_full_alert_sent = True
            battery_not_full_alert_sent = False
        elif consecutive_not_full_count >= CONSECUTIVE_NOT_FULL_CHECKS and not battery_not_full_alert_sent:
            send_telegram_message(get_text("battery_not_full"))
            battery_not_full_alert_sent = True
            battery_full_alert_sent = False

    except KeyError as e:
        logging.error(f"Missing data field: {e}")

if __name__ == "__main__":
    logging.info(get_text("bot_start"))
    send_telegram_message(get_text("bot_start"))
    
    # Immediate first check
    data = fetch_solar_data()
    if data:
        try:
            battery_mode = data["Body"]["Data"]["Inverters"]["1"].get("Battery_Mode", "")
            battery_is_full = battery_mode == "battery full"
            
            if battery_is_full:
                send_telegram_message(get_text("battery_full"))
                battery_full_alert_sent = True
                battery_not_full_alert_sent = False
            else:
                send_telegram_message(get_text("battery_not_full"))
                battery_not_full_alert_sent = True
                battery_full_alert_sent = False
        except KeyError as e:
            logging.error(f"Missing data field on startup: {e}")
    
    while True:
        check_solar_data()
        time.sleep(CHECK_INTERVAL)
