import requests
import json
import os
from datetime import datetime

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

if status == "success":
    color = "good"
else:
    color = "danger"

current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

footer_text = f"Created by {actor} • {current_time}"
footer_icon_url = f"https://github.com/{actor}.png"

payload = {
    "attachments": [
        {
            "fallback": title,
            "color": color,
            "title": title,
            "text": description,
            "footer": footer_text,
            "footer_icon": f"https://github.com/{actor}.png",
        }
    ],
}

if fields:
    fields_list = serialize_fields(fields)
    payload["attachments"][0]["fields"] = fields_list

headers = {"Content-Type": "application/json"}
data = json.dumps(payload)

response = requests.post(webhook_url, data=data, headers=headers)

print(data)
if response.status_code == 200:
    print("Message sent to Slack successfully!")
else:
    print(f"Failed to send message to Slack. Status code: {response.status_code}")
    print(response.text)
