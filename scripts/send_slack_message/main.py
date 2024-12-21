import requests
import json
import re
import os

from serialize_fields import serialize_fields

webhook_url = os.getenv("SLACK_WEBHOOK_URL")
title = os.getenv("TITLE")
description = os.getenv("DESCRIPTION")
status = os.getenv("STATUS")
actor = os.getenv("ACTOR")
fields = os.getenv("FIELDS") or ""
components = os.getenv("COMPONENTS") or None
debug = os.getenv("DEBUG") == "true" or False

if debug:
    print(f"Webhook URL: {webhook_url}")
    print(f"Title: {title}")
    print(f"Description: {description}")
    print(f"Status: {status}")
    print(f"Actor: {actor}")
    print(f"Fields: {fields}")
    print(f"Components: {components}")
    debug = True

if status == "success":
    color = 3066993
else:
    color = 15158332

footer_text = f"Created by @{actor} • %{{now('%Y/%m/%d %H:%M')}}"
footer_icon_url = f"https://github.com/{actor}.png"


payload = {
    "attachments": [
        {
            "fallback": title,
            "color": color,
            "title": title,
            "text": description,
            "footer": footer_text,
            "footer_icon": footer_icon_url,
        }
    ],
}

if fields:
    payload["attachments"][0]["fields"] = serialize_fields(fields)

headers = {"Content-Type": "application/json"}
data = json.dumps(payload)

response = requests.post(webhook_url, data=data, headers=headers)

print(data)
if response.status_code == 204:
    print("Message sent to Slack successfully!")
else:
    print(f"Failed to send message to Slack. Status code: {response.status_code}")
    print(response.text)
