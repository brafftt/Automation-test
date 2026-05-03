#!/usr/bin/env python3
"""
Main orchestrator for Meta Ads to Newsletter automation.
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import load_env, create_logger
from src.integrations.meta_ads import MetaAdsClient
from src.integrations.ghl import GHLClient
from src.integrations.slack_notifier import SlackNotifier
from src.newsletter.generator import NewsletterGenerator

logger = create_logger(__name__)

class NewsletterOrchestrator:
    """Orchestrate the complete newsletter workflow."""

    def __init__(self):
        logger.info("Initializing orchestrator")
        self.env = load_env()
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize all API clients."""
        logger.info("Initializing API clients")

        self.meta_client = MetaAdsClient(
            self.env["META_ACCESS_TOKEN"],
            self.env["META_BUSINESS_ACCOUNT_ID"]
        )

        self.ghl_client = GHLClient(
            self.env["GHL_API_KEY"],
            self.env["GHL_BUSINESS_ID"]
        )

        self.slack_notifier = SlackNotifier(
            self.env["SLACK_CHANNEL_ID"]
        )

        self.newsletter_generator = NewsletterGenerator()

    def run(self) -> bool:
        """Execute the complete workflow."""
        logger.info("=" * 50)
        logger.info("Starting Newsletter Workflow")
        logger.info("=" * 50)

        try:
            logger.info("Step 1: Fetching Meta Ads insights...")
            insights = self._fetch_insights()

            if not insights:
                logger.warning("No insights found")
                self.slack_notifier.notify_error(
                    "No campaigns found in Meta Ads",
                    {"stage": "fetch", "campaign_count": 0}
                )
                return False

            logger.info("Step 2: Processing and filtering data...")
            processed = self._process_insights(insights)

            if not processed:
                logger.warning("No items passed performance filter")
                self.slack_notifier.notify_error(
                    "No campaigns met performance threshold",
                    {"stage": "filter", "threshold": 0.7}
                )
                return False

            logger.info("Step 3: Ranking and selecting top items...")
            top_items = self.newsletter_generator.rank_items(processed)

            logger.info("Step 4: Generating newsletter HTML...")
            email_data = self._generate_newsletter(top_items)

            logger.info("Step 5: Scheduling email in GHL...")
            email_id = self._schedule_email(email_data)

            logger.info("Step 6: Sending Slack notification...")
            self._notify_success(len(insights), len(top_items), email_id)

            logger.info("=" * 50)
            logger.info("✅ Workflow completed successfully!")
            logger.info("=" * 50)

            return True

        except Exception as e:
            logger.error(f"Workflow failed: {e}", exc_info=True)
            self._notify_error(str(e))
            return False

    def _fetch_insights(self) -> list:
        """Fetch insights from Meta Ads API."""
        try:
            insights = self.meta_client.get_all_insights("LAST_30_DAYS")
            logger.info(f"Fetched {len(insights)} campaign insights")
            return insights
        except Exception as e:
            logger.error(f"Failed to fetch insights: {e}")
            raise

    def _process_insights(self, insights: list) -> list:
        """Process and filter insights."""
        try:
            processed = self.newsletter_generator.process_insights(insights)
            filtered = self.newsletter_generator.rank_items(
                [i for i in processed if i.get("performance_score", 0) >= 0.7]
            )
            logger.info(f"Processed {len(processed)} insights, {len(filtered)} passed filter")
            return filtered
        except Exception as e:
            logger.error(f"Failed to process insights: {e}")
            raise

    def _generate_newsletter(self, items: list) -> Dict:
        """Generate newsletter content."""
        try:
            email_data = self.newsletter_generator.get_email_body(
                items,
                title="📊 Weekly Performance Digest",
                subtitle="Your Best Performing Campaigns",
                company_name="Your Company"
            )
            logger.info("Newsletter generated successfully")
            return email_data
        except Exception as e:
            logger.error(f"Failed to generate newsletter: {e}")
            raise

    def _schedule_email(self, email_data: Dict) -> str:
        """Schedule email in GHL."""
        try:
            contact_id = self.ghl_client.get_or_create_contact(
                email=self.env.get("NEWSLETTER_FROM_EMAIL", "test@example.com"),
                name="Newsletter Contact"
            )

            scheduled_at = (datetime.now() + timedelta(days=1)).isoformat()

            email_id = self.ghl_client.schedule_email(
                contact_id=contact_id,
                subject=email_data["subject"],
                body=email_data["html"],
                scheduled_at=scheduled_at,
                from_name=email_data.get("from_name", "Newsletter"),
                from_email=email_data.get("from_email", "")
            )

            logger.info(f"Email scheduled: {email_id}")
            return email_id

        except Exception as e:
            logger.error(f"Failed to schedule email: {e}")
            raise

    def _notify_success(self, campaign_count: int, item_count: int, email_id: str):
        """Send success notification to Slack."""
        try:
            self.slack_notifier.notify_success(
                "Newsletter Ready",
                {
                    "campaign_count": campaign_count,
                    "item_count": item_count,
                    "email_id": email_id,
                    "scheduled_at": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                    "performance_score": "0.85"
                }
            )
            logger.info("Success notification sent")
        except Exception as e:
            logger.warning(f"Failed to send Slack notification: {e}")

    def _notify_error(self, error: str):
        """Send error notification to Slack."""
        try:
            self.slack_notifier.notify_error(
                error,
                {
                    "stage": "unknown",
                    "timestamp": datetime.now().isoformat()
                }
            )
            logger.info("Error notification sent")
        except Exception as e:
            logger.warning(f"Failed to send error notification: {e}")

def main():
    """Main entry point."""
    try:
        orchestrator = NewsletterOrchestrator()
        success = orchestrator.run()

        sys.exit(0 if success else 1)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
