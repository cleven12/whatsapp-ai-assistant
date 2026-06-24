import requests
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    """Wrapper around WhatsApp Cloud Business API for sending messages."""

    API_VERSION = "v21.0"

    def __init__(self):
        cfg = current_app.config
        self.token = cfg['WHATSAPP_TOKEN']
        self.phone_number_id = cfg['WHATSAPP_PHONE_NUMBER_ID']
        self.url = f"https://graph.facebook.com/{self.API_VERSION}/{self.phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def send_message(self, recipient_number, message_text):
        """
        Send a plain text message to a WhatsApp user.
        Returns response JSON or None on failure.
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_number,
            "type": "text",
            "text": {"preview_url": False, "body": message_text}
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=15)
            response.raise_for_status()
            logger.info(f"Message sent successfully to {recipient_number}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            return None

    def send_template_message(self, recipient_number, template_name, language_code="en_US"):
        """Placeholder for future rich template messaging support."""
        logger.info("Template messaging not yet implemented")
        return None
