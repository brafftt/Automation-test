import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from src.utils import create_logger

logger = create_logger(__name__)

class MetaAdsClient:
    """Client for Meta Ads API."""

    BASE_URL = "https://graph.instagram.com/v18.0"

    def __init__(self, access_token: str, business_account_id: str):
        self.access_token = access_token
        self.business_account_id = business_account_id
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make HTTP request to Meta API."""
        url = f"{self.BASE_URL}/{endpoint}"

        if params is None:
            params = {}
        params["access_token"] = self.access_token

        try:
            response = requests.request(method, url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Meta API request failed: {e}")
            raise

    def get_campaigns(self, limit: int = 100) -> List[Dict]:
        """Get all campaigns for the business account."""
        logger.info(f"Fetching campaigns for account {self.business_account_id}")

        params = {
            "fields": "id,name,status,created_time",
            "limit": limit
        }

        result = self._make_request(
            "GET",
            f"{self.business_account_id}/campaigns",
            params
        )

        campaigns = result.get("data", [])
        logger.info(f"Found {len(campaigns)} campaigns")

        return campaigns

    def get_campaign_insights(self, campaign_id: str, date_preset: str = "LAST_30_DAYS") -> Dict:
        """Get insights for a specific campaign."""
        logger.debug(f"Fetching insights for campaign {campaign_id}")

        fields = [
            "spend",
            "impressions",
            "clicks",
            "reach",
            "frequency",
            "actions",
            "ctr",
            "cpc",
            "cpm"
        ]

        params = {
            "fields": ",".join(fields),
            "date_preset": date_preset
        }

        result = self._make_request("GET", f"{campaign_id}/insights", params)

        data = result.get("data", [])
        if data:
            return {
                "campaign_id": campaign_id,
                **data[0]
            }
        return {}

    def get_all_insights(self, date_preset: str = "LAST_30_DAYS") -> List[Dict]:
        """Get insights for all campaigns."""
        logger.info("Fetching insights for all campaigns")

        campaigns = self.get_campaigns()
        all_insights = []

        for campaign in campaigns:
            try:
                insights = self.get_campaign_insights(campaign["id"], date_preset)
                if insights:
                    insights["campaign_name"] = campaign["name"]
                    insights["campaign_status"] = campaign["status"]
                    all_insights.append(insights)
            except Exception as e:
                logger.warning(f"Failed to fetch insights for campaign {campaign['id']}: {e}")

        logger.info(f"Retrieved insights for {len(all_insights)} campaigns")
        return all_insights

    def filter_by_performance(self, insights: List[Dict], threshold: float = 0.7) -> List[Dict]:
        """Filter insights by performance score."""
        logger.info(f"Filtering insights with threshold {threshold}")

        filtered = []

        for item in insights:
            score = self._calculate_performance_score(item)
            if score >= threshold:
                item["performance_score"] = score
                filtered.append(item)

        logger.info(f"Filtered {len(filtered)} items with score >= {threshold}")
        return filtered

    @staticmethod
    def _calculate_performance_score(insights: Dict) -> float:
        """Calculate performance score based on metrics."""
        try:
            spend = float(insights.get("spend", 0) or 0)
            clicks = float(insights.get("clicks", 0) or 0)
            reach = float(insights.get("reach", 0) or 0)
            actions = float(insights.get("actions", 0) or 0)

            if spend == 0:
                return 0

            roas = actions / spend if spend > 0 else 0
            cpc = spend / clicks if clicks > 0 else float("inf")
            reach_efficiency = reach / spend if spend > 0 else 0

            score = (roas * 0.5 + (1 / cpc) * 0.3 + reach_efficiency * 0.2) / 10

            return min(1.0, score)
        except:
            return 0
