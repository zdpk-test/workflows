import requests
import json
import re

webhook_url = '${{ inputs.discord_webhook_url }}'
title = '${{ inputs.title }}'
description = '${{ inputs.description }}' or ''
status = '${{ inputs.status }}'
actor = '${{ inputs.actor }}'
fields = '${{ inputs.fields }}'
components = '${{ inputs.components }}' or {}
debug = '${{ inputs.debug }}' or False

if debug == 'true':
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
   fields_list = []
   for line in fields.strip().splitlines():
        line = line.strip()
        field_items = re.split(r',\s*(?=[^\s])', line)
        row = []
        for item in field_items:
            if ":" in item:
               key, value = item.split(":", 1)
               row.append({"name": key.strip(), "value": value.strip(), "inline": True})
        if row:
           fields_list.extend(row)
   payload["embeds"][0]["fields"] = fields_list


if components:
   payload["components"] = json.loads(components)

headers = {'Content-Type': 'application/json'}
response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

if response.status_code == 204:
 print("Message sent to Discord successfully!")
else:
 print(f"Failed to send message to Discord. Status code: {response.status_code}")
 print(response.text)