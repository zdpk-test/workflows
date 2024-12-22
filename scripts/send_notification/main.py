from send_notification import send_notification
from payload import create_payload

platforms = ["discord", "slack"]

if __name__ == "__main__":
    for platform in platforms:
        payload = create_payload(platform)
        send_notification(payload)
