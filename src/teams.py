import requests

def send_to_teams(webhook_url: str, card_payload: dict):
    resp = requests.post(webhook_url, json=card_payload, timeout=10)
    resp.raise_for_status()
    return resp.status_code
