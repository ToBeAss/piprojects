import requests

def send_to_teams(webhook_url: str, payload: dict):
    """Try Adaptive Card first; on failure fall back to simple text."""
    try:
        r = requests.post(webhook_url, json=payload, timeout=10)
        r.raise_for_status()
        return ("adaptive", r.status_code, None)
    except Exception as e:
        # Fallback: plain text so we still see something in the channel
        try:
            fallback = {"text": payload.get("fallback_text", "Soil moisture update")}
            r2 = requests.post(webhook_url, json=fallback, timeout=10)
            r2.raise_for_status()
            return ("fallback", r2.status_code, str(e))
        except Exception as e2:
            return ("error", None, f"adaptive_err={e}; fallback_err={e2}")
