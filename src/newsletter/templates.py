"""Email templates for newsletters."""

STYLES = """
<style>
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        background-color: #f9f9f9;
    }
    .container {
        max-width: 600px;
        margin: 0 auto;
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        text-align: center;
        border-radius: 8px 8px 0 0;
        margin: -20px -20px 20px -20px;
    }
    .header h1 {
        margin: 0;
        font-size: 28px;
    }
    .item {
        border-left: 4px solid #667eea;
        padding: 15px;
        margin: 15px 0;
        background-color: #f5f5f5;
        border-radius: 4px;
    }
    .item-title {
        font-size: 18px;
        font-weight: bold;
        color: #333;
        margin: 0 0 10px 0;
    }
    .metrics {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 10px 0;
    }
    .metric {
        background-color: white;
        padding: 10px;
        border-radius: 4px;
        border: 1px solid #ddd;
    }
    .metric-label {
        font-size: 12px;
        color: #999;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 16px;
        font-weight: bold;
        color: #667eea;
    }
    .badge {
        display: inline-block;
        padding: 4px 8px;
        margin: 4px 4px 4px 0;
        background-color: #e0e7ff;
        color: #667eea;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        padding-top: 20px;
        border-top: 1px solid #ddd;
        font-size: 12px;
        color: #999;
        margin-top: 20px;
    }
    .cta {
        text-align: center;
        margin: 20px 0;
    }
    .cta-button {
        display: inline-block;
        padding: 12px 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-decoration: none;
        border-radius: 4px;
        font-weight: bold;
    }
</style>
"""

DEFAULT_TEMPLATE = """
{%- set styles = styles %}
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title }}</title>
    {{ styles }}
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 {{ title }}</h1>
            <p>{{ subtitle }}</p>
        </div>

        <p>Hi there,</p>

        <p>{{ introduction }}</p>

        {%- for item in items %}
        <div class="item">
            <div class="item-title">{{ item.title }}</div>
            <p>{{ item.description }}</p>

            <div class="metrics">
                {%- for metric in item.key_metrics %}
                <div class="metric">
                    <div class="metric-label">{{ metric.label }}</div>
                    <div class="metric-value">{{ metric.value }}</div>
                </div>
                {%- endfor %}
            </div>

            {%- if item.badges %}
            <div>
                {%- for badge in item.badges %}
                <span class="badge">{{ badge }}</span>
                {%- endfor %}
            </div>
            {%- endif %}
        </div>
        {%- endfor %}

        {%- if call_to_action %}
        <div class="cta">
            <a href="{{ cta_url }}" class="cta-button">{{ call_to_action }}</a>
        </div>
        {%- endif %}

        <div class="footer">
            <p>{{ footer_text }}</p>
            <p>© {{ current_year }} {{ company_name }}. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

MINIMAL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    {{ styles }}
</head>
<body>
    <div class="container">
        <h2>{{ title }}</h2>

        {%- for item in items %}
        <h3>{{ item.title }}</h3>
        <p>{{ item.description }}</p>

        {%- if item.key_metrics %}
        <ul>
        {%- for metric in item.key_metrics %}
            <li><strong>{{ metric.label }}:</strong> {{ metric.value }}</li>
        {%- endfor %}
        </ul>
        {%- endif %}
        {%- endfor %}

        <hr>
        <p>{{ footer_text }}</p>
    </div>
</body>
</html>
"""

TEMPLATES = {
    "default": DEFAULT_TEMPLATE,
    "minimal": MINIMAL_TEMPLATE
}

def get_template(name: str = "default") -> str:
    """Get template by name."""
    return TEMPLATES.get(name, DEFAULT_TEMPLATE)
