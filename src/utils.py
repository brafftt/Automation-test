import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

def load_env() -> Dict[str, str]:
    """Load environment variables from settings."""
    config_path = ".claude/settings.local.json"

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}\n"
            "Please create it with your API credentials."
        )

    with open(config_path, "r") as f:
        config = json.load(f)

    env = config.get("env", {})

    required_keys = [
        "META_ACCESS_TOKEN",
        "META_BUSINESS_ACCOUNT_ID",
        "GHL_API_KEY",
        "GHL_BUSINESS_ID",
        "SLACK_BOT_TOKEN",
        "SLACK_CHANNEL_ID"
    ]

    missing = [key for key in required_keys if key not in env]
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")

    return env

def create_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Create and configure a logger."""
    logger = logging.getLogger(name)

    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

def format_number(value: float, decimals: int = 2) -> str:
    """Format number with thousands separator."""
    return f"{value:,.{decimals}f}"

def parse_date(date_str: str) -> datetime:
    """Parse ISO 8601 date string."""
    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))

def format_currency(value: float) -> str:
    """Format value as currency."""
    return f"${format_number(value)}"

def calculate_percentage(part: float, total: float) -> float:
    """Calculate percentage."""
    return (part / total * 100) if total > 0 else 0

def sanitize_html(html: str) -> str:
    """Basic HTML sanitization."""
    dangerous = ["<script", "javascript:", "onerror=", "onclick="]
    for item in dangerous:
        html = html.replace(item, "")
    return html

def get_env_with_default(key: str, default: Any = None) -> Any:
    """Get environment variable with default."""
    try:
        env = load_env()
        return env.get(key, default)
    except:
        return default

def validate_email(email: str) -> bool:
    """Validate email format (basic)."""
    return "@" in email and "." in email.split("@")[1]

def truncate_string(text: str, length: int = 100) -> str:
    """Truncate string to specified length."""
    return text[:length] + "..." if len(text) > length else text
