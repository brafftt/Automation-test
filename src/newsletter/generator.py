from typing import List, Dict, Optional
from jinja2 import Template
from datetime import datetime
from src.newsletter.templates import get_template, STYLES
from src.utils import format_currency, format_number, create_logger

logger = create_logger(__name__)

class NewsletterGenerator:
    """Generate newsletters from campaign insights."""

    def __init__(self, template_name: str = "default"):
        self.template_name = template_name
        self.max_items = 5
        self.min_performance_threshold = 0.7

    def process_insights(self, insights: List[Dict]) -> List[Dict]:
        """Process and structure insights for newsletter."""
        logger.info(f"Processing {len(insights)} insights")

        processed = []

        for insight in insights:
            try:
                item = self._process_single_insight(insight)
                if item:
                    processed.append(item)
            except Exception as e:
                logger.warning(f"Failed to process insight: {e}")

        logger.info(f"Processed {len(processed)} items")
        return processed

    def rank_items(self, items: List[Dict]) -> List[Dict]:
        """Rank items by performance score."""
        logger.info(f"Ranking {len(items)} items")

        ranked = sorted(
            items,
            key=lambda x: x.get("performance_score", 0),
            reverse=True
        )

        top_items = ranked[:self.max_items]

        logger.info(f"Selected top {len(top_items)} items")
        return top_items

    def generate_html(self, items: List[Dict], **kwargs) -> str:
        """Generate HTML newsletter from items."""
        logger.info(f"Generating HTML for {len(items)} items")

        template_str = get_template(self.template_name)

        context = {
            "styles": STYLES,
            "title": kwargs.get("title", "📊 Weekly Performance Report"),
            "subtitle": kwargs.get("subtitle", "Your Top Performing Campaigns"),
            "introduction": kwargs.get(
                "introduction",
                "Here are your top-performing campaigns this week. "
                "These campaigns achieved excellent ROI and engagement metrics."
            ),
            "items": items,
            "call_to_action": kwargs.get("call_to_action", "View Full Report"),
            "cta_url": kwargs.get("cta_url", "https://example.com"),
            "footer_text": kwargs.get(
                "footer_text",
                "This is an automated weekly report. "
                "You can customize these reports in your dashboard."
            ),
            "company_name": kwargs.get("company_name", "Your Company"),
            "current_year": datetime.now().year
        }

        template = Template(template_str)
        html = template.render(**context)

        logger.info(f"Generated HTML ({len(html)} characters)")
        return html

    def get_email_body(self, items: List[Dict], **kwargs) -> Dict:
        """Get complete email body with subject and HTML."""
        logger.info("Building email body")

        subject = kwargs.get(
            "subject",
            f"📊 Weekly Report - {datetime.now().strftime('%B %d, %Y')}"
        )

        html = self.generate_html(items, **kwargs)

        plain_text = self._generate_plain_text(items)

        return {
            "subject": subject,
            "html": html,
            "text": plain_text,
            "from_name": kwargs.get("from_name", "Newsletter"),
            "from_email": kwargs.get("from_email", "no-reply@example.com")
        }

    def _process_single_insight(self, insight: Dict) -> Optional[Dict]:
        """Process a single insight into newsletter item."""
        try:
            spend = float(insight.get("spend", 0) or 0)
            clicks = float(insight.get("clicks", 0) or 0)
            impressions = float(insight.get("impressions", 0) or 0)
            reach = float(insight.get("reach", 0) or 0)
            actions = float(insight.get("actions", 0) or 0)

            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            cpc = spend / clicks if clicks > 0 else 0
            cpm = (spend / impressions * 1000) if impressions > 0 else 0
            roas = actions / spend if spend > 0 else 0

            performance_score = insight.get("performance_score", 0)

            metrics = []

            if roas > 0:
                metrics.append({
                    "label": "ROAS",
                    "value": f"{roas:.2f}x"
                })

            metrics.append({
                "label": "Impressions",
                "value": f"{impressions:,.0f}"
            })

            metrics.append({
                "label": "CTR",
                "value": f"{ctr:.2f}%"
            })

            if cpc < float("inf"):
                metrics.append({
                    "label": "CPC",
                    "value": format_currency(cpc)
                })

            badges = []
            if roas >= 3:
                badges.append("💰 High ROI")
            if ctr >= 5:
                badges.append("📈 High CTR")
            if reach >= 50000:
                badges.append("🎯 Wide Reach")

            return {
                "title": insight.get("campaign_name", "Campaign"),
                "description": f"Campaign achieved excellent performance this period with {format_number(cpc)} cost per click.",
                "key_metrics": metrics,
                "badges": badges,
                "performance_score": performance_score,
                "spend": spend,
                "clicks": clicks,
                "roas": roas
            }
        except Exception as e:
            logger.warning(f"Error processing insight: {e}")
            return None

    def _generate_plain_text(self, items: List[Dict]) -> str:
        """Generate plain text version of newsletter."""
        lines = ["Weekly Performance Report\n"]

        for item in items:
            lines.append(f"\n{item['title']}")
            lines.append("-" * len(item['title']))
            lines.append(item['description'])

            for metric in item.get("key_metrics", []):
                lines.append(f"  • {metric['label']}: {metric['value']}")

        lines.append("\n\nEnd of Report")

        return "\n".join(lines)

    def validate_items(self, items: List[Dict]) -> bool:
        """Validate that items are properly formatted."""
        logger.info(f"Validating {len(items)} items")

        if not items:
            logger.warning("No items to validate")
            return False

        required_fields = ["title", "description", "key_metrics"]

        for item in items:
            for field in required_fields:
                if field not in item:
                    logger.warning(f"Missing field {field} in item")
                    return False

        logger.info("All items valid")
        return True
