from datetime import datetime
import json
from serialize_fields import serialize_fields

import os


class Payload:
    def __init__(
        self,
        title,
        description,
        status,
        actor,
        fields,
        components,
        platform,
        webhook_url,
    ):
        self.title = title
        self.description = description
        self.status = status
        self.actor = actor
        self.fields = fields
        self.components = components
        self.platform = platform
        self.webhook_url = webhook_url

    def _status_color(self):
        if self.platform == "discord":
            if self.status == "success":
                return 3066993
            if self.status == "failure":
                return 15158332

        if self.platform == "slack":
            if self.status == "success":
                return "good"
            if self.status == "failure":
                return "danger"

    def _to_discord_data(self, footer_text: str, footer_icon_url: str) -> str:
        payload = {
            "embeds": [
                {
                    "title": f"##{self.title}",
                    "description": self.description,
                    "color": self._status_color(),
                    "footer": {"text": footer_text, "icon_url": footer_icon_url},
                }
            ],
        }

        if self.fields:
            payload["embeds"][0]["fields"] = serialize_fields(self.fields)

        return json.dumps(payload)

    def _to_slack_data(self, footer_text: str, footer_icon_url: str) -> str:
        return {
            "attachments": [
                {
                    "fallback": self.title,
                    "color": self._status_color(),
                    "title": self.title,
                    "text": self.description,
                    "footer": footer_text,
                    "footer_icon": footer_icon_url,
                }
            ]
        }

    def to_data(self) -> str:
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        footer_text = f"Created by {self.actor} • {now}"
        footer_icon_url = f"https://github.com/{self.actor}.png"

        if self.platform == "slack":
            return self._to_slack_data(now, footer_text, footer_icon_url)

        if self.platform == "discord":
            return self._to_discord_data(now, footer_text, footer_icon_url)

        raise ValueError("Invalid platform - must be either 'discord' or 'slack'")


def create_payload(platform: str) -> Payload | None:
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    title = os.getenv("TITLE")
    description = os.getenv("DESCRIPTION")
    status = os.getenv("STATUS")
    actor = os.getenv("ACTOR")
    fields = os.getenv("FIELDS")
    components = os.getenv("COMPONENTS")
    debug = os.getenv("DEBUG") == "true" or False

    if platform == "discord" and discord_webhook_url is None:
        return None
    if platform == "slack" and slack_webhook_url is None:
        return None

    return Payload(title, description, status, actor, fields, components, platform)
