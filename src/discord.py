import requests

def send_to_discord(webhook: str, content: str):
    data = {
        "content": content
    }

    try:
        response = requests.post(webhook, json=data, timeout=10)  # Add timeout

        if response.status_code == 204:
            print("Message sent to Discord successfully.")
            return True
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Discord webhook error: {e}")
        return False