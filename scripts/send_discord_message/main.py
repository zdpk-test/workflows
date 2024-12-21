import requests
import json
import re
import os

from serialize_fields import serialize_fields

webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
title = os.getenv('TITLE')
description = os.getenv('DESCRIPTION')
status = os.getenv('STATUS')
actor = os.getenv('ACTOR')
fields = os.getenv('FIELDS') or ''
components = os.getenv('COMPONENTS') or None
debug = os.getenv('DEBUG') == 'true' or False

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
   "embeds": [{
       "title": title,
       "description": description,
       "color": color,
        "footer": {
           "text": footer_text,
          "icon_url": footer_icon_url
        }
   }],
}

if fields:
   payload['embeds'][0]['fields'] = serialize_fields(fields)

# if components:
#    payload["components"] = json.loads(components)

headers = {'Content-Type': 'application/json'}
response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

if response.status_code == 204:
 print("Message sent to Discord successfully!")
else:
 print(f"Failed to send message to Discord. Status code: {response.status_code}")
 print(response.text)