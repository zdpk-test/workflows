import requests
from payload import Payload


def send_notification(payload: Payload | None, retry_count: int = 3):
    if payload is None:
        return

    headers = {"Content-Type": "application/json"}

    try:
        resp = requests.post(
            payload.webhook_url, data=payload.to_data(), headers=headers
        )

        if resp.status_code == 204:
            print("Message sent to Discord successfully!")
        else:
            raise Exception(f"Failed to send message. Status code: {resp.status_code}")
    except Exception as e:
        print(e)
        retry_count -= 1
        if retry_count > 0:
            print(f"Retrying... ({retry_count} attempts left)")
            send_notification(payload, retry_count)
        else:
            print(f"Failed to send message. Status code: {resp.status_code}")
            print(resp.text)
            raise
