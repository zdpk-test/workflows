import requests
from payload import Payload


def send_notification(payload: Payload | None):
    if payload == None:
        return

    headers = {"Content-Type": "application/json"}

    resp = requests.post(payload.webhook_url, data=payload.to_data(), headers=headers)

    if resp.status_code == 204:
        print("Message sent to Discord successfully!")
    else:
        print(f"Failed to send message. Status code: {resp.status_code}")
        print(resp.text)
