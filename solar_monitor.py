import time
import json
import requests
import logging

# Load configuration from JSON
with open("config.json", "r") as file:
    config = json.load(file)

# Telegram Bot details
TELEGRAM_TOKEN = config["telegram_token"]
CHAT_ID = config["chat_id"]

# Hardcoded API path with dynamic IP
SOLAR_API_IP = config["solar_api_ip"]
API_URL = f"http://{SOLAR_API_IP}/solar_api/v1/GetPowerFlowRealtimeData.fcgi"

# Convert minutes to seconds
CONDITION_DURATION = config["condition_duration_min"] * 60
CHECK_INTERVAL = config["check_interval_min"] * 60

# Variables to track the condition state
excess_condition_start = None
excess_alert_sent = False

consumption_condition_start = None
consumption_alert_sent = False

# Set up logging
logging.basicConfig(
    filename="solar_monitor.log",
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
        logging.info("Telegram message sent successfully")
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
    """Checks solar power conditions and sends alerts if needed."""
    global excess_condition_start, excess_alert_sent, consumption_condition_start, consumption_alert_sent
    data = fetch_solar_data()

    if not data:
        return

    try:
        soc = data["Body"]["Data"]["Inverters"]["1"].get("SOC", 0)
        p_pv = data["Body"]["Data"]["Site"].get("P_PV", 0)
        p_load = abs(data["Body"]["Data"]["Site"].get("P_Load", 0))

        # Define conditions
        excess_condition_met = soc > 97 and p_pv > p_load
        consumption_condition_met = p_load > p_pv and soc < 97
        current_time = time.time()

        # Handle excess solar production alert
        if excess_condition_met:
            if excess_condition_start is None:
                excess_condition_start = current_time
            if (current_time - excess_condition_start >= CONDITION_DURATION) and (not excess_alert_sent):
                send_telegram_message("Warning: Excess solar production or too little consumption!")
                excess_alert_sent = True
        else:
            excess_condition_start = None
            excess_alert_sent = False

        # Handle excessive consumption alert
        if consumption_condition_met:
            if consumption_condition_start is None:
                consumption_condition_start = current_time
            if (current_time - consumption_condition_start >= CONDITION_DURATION) and (not consumption_alert_sent):
                send_telegram_message("Warning: Consuming too much power!")
                consumption_alert_sent = True
        else:
            consumption_condition_start = None
            consumption_alert_sent = False

    except KeyError as e:
        logging.error(f"Missing data field: {e}")

if __name__ == "__main__":
    logging.info("Starting Solar Monitoring Bot...")
    while True:
        check_solar_data()
        time.sleep(CHECK_INTERVAL)
