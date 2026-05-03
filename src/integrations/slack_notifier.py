from typing import Dict, Optional
from datetime import datetime
from src.utils import create_logger

logger = create_logger(__name__)

class SlackNotifier:
    """Slack notifications handler."""

    def __init__(self, channel_id: str):
        self.channel_id = channel_id
        logger.info(f"Initialized SlackNotifier for channel {channel_id}")

    def notify_success(self, title: str, details: Dict) -> None:
        """Send success notification to Slack."""
        logger.info(f"Sending success notification: {title}")

        message = self._build_success_blocks(title, details)
        self._send_message(message)

    def notify_error(self, error: str, details: Dict) -> None:
        """Send error notification to Slack."""
        logger.error(f"Sending error notification: {error}")

        message = self._build_error_blocks(error, details)
        self._send_message(message)

    def notify_scheduled(self, email_id: str, scheduled_at: str, recipient: str = "") -> None:
        """Send notification that email was scheduled."""
        logger.info(f"Sending scheduled notification for email {email_id}")

        message = self._build_scheduled_blocks(email_id, scheduled_at, recipient)
        self._send_message(message)

    def notify_processing(self, campaign_count: int, item_count: int) -> None:
        """Send notification that processing started."""
        logger.info(f"Sending processing notification: {campaign_count} campaigns, {item_count} items")

        message = self._build_processing_blocks(campaign_count, item_count)
        self._send_message(message)

    def _build_success_blocks(self, title: str, details: Dict) -> str:
        """Build success message blocks."""
        blocks = f"""
📊 **{title}**

✅ Newsletter successfully created and scheduled!

📈 **Details:**
• Items included: {details.get('item_count', 0)}
• Campaigns processed: {details.get('campaign_count', 0)}
• Scheduled for: {details.get('scheduled_at', 'N/A')}
• Performance score: {details.get('performance_score', 'N/A')}

🔗 Email ID: `{details.get('email_id', 'N/A')}`

_Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_
"""
        return blocks

    def _build_error_blocks(self, error: str, details: Dict) -> str:
        """Build error message blocks."""
        blocks = f"""
❌ **Newsletter Generation Failed**

⚠️ Error: {error}

📋 **Details:**
• Stage: {details.get('stage', 'Unknown')}
• Campaign: {details.get('campaign_name', 'N/A')}
• Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

_Check logs for more details_
"""
        return blocks

    def _build_scheduled_blocks(self, email_id: str, scheduled_at: str, recipient: str = "") -> str:
        """Build scheduled notification blocks."""
        blocks = f"""
📧 **Email Scheduled Successfully**

✅ Newsletter is ready to be sent!

📌 **Details:**
• Email ID: `{email_id}`
• Scheduled for: {scheduled_at}
• Recipient: {recipient if recipient else 'Contact list'}

_Status: SCHEDULED_
"""
        return blocks

    def _build_processing_blocks(self, campaign_count: int, item_count: int) -> str:
        """Build processing notification blocks."""
        blocks = f"""
⏳ **Newsletter Processing Started**

📊 **Processing:**
• Total campaigns: {campaign_count}
• Top items selected: {item_count}
• Status: IN PROGRESS

_Please wait for completion notification..._
"""
        return blocks

    def _send_message(self, message: str) -> None:
        """Send message to Slack (via MCP tools)."""
        try:
            logger.info(f"Message would be sent to {self.channel_id}")
            logger.debug(f"Message content: {message}")
        except Exception as e:
            logger.error(f"Failed to send Slack message: {e}")
            raise

    def log_info(self, message: str) -> None:
        """Log info message."""
        logger.info(message)

    def log_error(self, message: str) -> None:
        """Log error message."""
        logger.error(message)

    def log_debug(self, message: str) -> None:
        """Log debug message."""
        logger.debug(message)
