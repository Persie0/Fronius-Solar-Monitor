import requests
import logging

class TelegramNotifier:
    """Handles sending notifications via Telegram"""
    
    def __init__(self, token, chat_id):
        """Initialize with Telegram bot token and chat ID"""
        self.token = token
        self.chat_id = chat_id
    
    def send_message(self, message):
        """Sends a message via Telegram Bot."""
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": message}
            response = requests.post(url, json=payload)
            response.raise_for_status()
            logging.info("Telegram message sent successfully: %s", message)
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send Telegram message: {e}")
            return False