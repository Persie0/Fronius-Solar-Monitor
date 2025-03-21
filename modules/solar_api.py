import requests
import logging

class SolarAPI:
    """Handles interactions with the Fronius Solar API"""
    
    def __init__(self, api_ip):
        """Initialize with the IP address of the Fronius inverter"""
        self.api_url = f"http://{api_ip}/solar_api/v1/GetPowerFlowRealtimeData.fcgi"
    
    def fetch_data(self):
        """Fetches real-time solar power data."""
        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching solar data: {e}")
            return None
    
    def get_battery_status(self, data):
        """Extracts battery status from API response data."""
        if not data:
            return None, None, False
            
        try:
            battery_mode = data["Body"]["Data"]["Inverters"]["1"].get("Battery_Mode", "")
            battery_soc = data["Body"]["Data"]["Inverters"]["1"].get("SOC", "Unknown")
            battery_is_full = battery_mode == "battery full"
            
            return battery_mode, battery_soc, battery_is_full
        except KeyError as e:
            logging.error(f"Missing data field: {e}")
            return None, None, False
            
    def get_pv_production(self, data):
        """Extracts current PV production in watts from API response data."""
        if not data:
            return 0
            
        try:
            # Get PV production value from the API response
            pv_production = data["Body"]["Data"]["Site"].get("P_PV", 0)
            return pv_production
        except KeyError as e:
            logging.error(f"Missing PV production data field: {e}")
            return 0