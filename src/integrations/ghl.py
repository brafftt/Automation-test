import requests
from typing import List, Dict, Optional
from src.utils import create_logger

logger = create_logger(__name__)

class GHLClient:
    """Client for GoHighLevel API."""

    BASE_URL = "https://api.gohighlevel.com/v1"

    def __init__(self, api_key: str, business_id: str):
        self.api_key = api_key
        self.business_id = business_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to GHL API."""
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = requests.request(
                method,
                url,
                json=data,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"GHL API request failed: {e}")
            raise

    def get_contacts(self, limit: int = 50) -> List[Dict]:
        """Get list of contacts."""
        logger.info(f"Fetching contacts (limit: {limit})")

        result = self._make_request(
            "GET",
            f"contacts?limit={limit}"
        )

        contacts = result.get("data", [])
        logger.info(f"Found {len(contacts)} contacts")

        return contacts

    def create_contact(self, email: str, name: str = "", phone: str = "") -> Dict:
        """Create a new contact."""
        logger.info(f"Creating contact: {email}")

        data = {
            "email": email,
            "firstName": name.split()[0] if name else "",
            "lastName": " ".join(name.split()[1:]) if name else "",
            "phone": phone
        }

        result = self._make_request("POST", "contacts", data)

        if result.get("success"):
            logger.info(f"Contact created: {result['data']['id']}")
            return result.get("data", {})
        else:
            raise Exception(f"Failed to create contact: {result.get('error')}")

    def get_contact(self, contact_id: str) -> Dict:
        """Get contact by ID."""
        logger.debug(f"Fetching contact {contact_id}")

        result = self._make_request("GET", f"contacts/{contact_id}")

        if result.get("success"):
            return result.get("data", {})
        else:
            raise Exception(f"Contact not found: {contact_id}")

    def schedule_email(self, contact_id: str, subject: str, body: str,
                      scheduled_at: str, from_name: str = "Newsletter",
                      from_email: str = "") -> str:
        """Schedule an email for a contact."""
        logger.info(f"Scheduling email to contact {contact_id}")

        data = {
            "contactId": contact_id,
            "subject": subject,
            "body": body,
            "scheduledAt": scheduled_at,
            "fromName": from_name,
            "fromEmail": from_email
        }

        result = self._make_request("POST", "emails", data)

        if result.get("success"):
            email_id = result.get("data", {}).get("id")
            logger.info(f"Email scheduled: {email_id}")
            return email_id
        else:
            raise Exception(f"Failed to schedule email: {result.get('error')}")

    def get_campaign_status(self, campaign_id: str) -> Dict:
        """Get campaign status."""
        logger.debug(f"Fetching campaign status: {campaign_id}")

        result = self._make_request("GET", f"campaigns/{campaign_id}")

        if result.get("success"):
            return result.get("data", {})
        else:
            raise Exception(f"Campaign not found: {campaign_id}")

    def get_or_create_contact(self, email: str, name: str = "") -> str:
        """Get existing contact or create new one."""
        logger.info(f"Getting or creating contact: {email}")

        contacts = self.get_contacts()

        for contact in contacts:
            if contact.get("email") == email:
                logger.info(f"Contact already exists: {contact['id']}")
                return contact["id"]

        new_contact = self.create_contact(email, name)
        return new_contact.get("id")
