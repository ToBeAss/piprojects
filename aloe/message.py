import math
import random
from typing import List, Dict
from aloe.personality import comments, emojis

def random_from_list(array):
    return array[math.floor(random.random() * len(array))]

def create_message(daily_data: List[Dict[str, int]]):
    if len(daily_data) == 0:
        return "No data from the last 24 hours."

    average = round(sum(item["moisture"] for item in daily_data) / len(daily_data))

    if average < 20:
        comment = random_from_list(comments.very_dry)
        emoji = random_from_list(emojis.dry)
    elif average < 40:
        comment = random_from_list(comments.dry)
        emoji = random_from_list(emojis.dry)
    elif average < 60:
        comment = random_from_list(comments.ok)
        emoji = random_from_list(emojis.ok)
    elif average < 80:
        comment = random_from_list(comments.wet)
        emoji = random_from_list(emojis.wet)
    else:
        comment = random_from_list(comments.very_wet)
        emoji = random_from_list(emojis.wet)

    summary_lines = ""
    previous_summary_value = daily_data[0]["moisture"] if daily_data else None
    for item in daily_data:
        if item['hour'] % 3 == 0 and item['hour'] != 0:

            hour_emoji = ""
            if item['hour'] == 24 or item['hour'] == 12:
                hour_emoji = "🕛 "
            elif item['hour'] == 3 or item['hour'] == 15:
                hour_emoji = "🕒 "
            elif item['hour'] == 6 or item['hour'] == 18:
                hour_emoji = "🕕 "
            elif item['hour'] == 9 or item['hour'] == 21:
                hour_emoji = "🕘 "

            change_emoji = "➖"
            if previous_summary_value is not None:
                if item['moisture'] > previous_summary_value:
                    change_emoji = "🔼"
                elif item['moisture'] < previous_summary_value:
                    change_emoji = "🔽"

            summary_lines += f"- {hour_emoji}{item['hour']:02d} - {item['moisture']}% {change_emoji}\n"
            previous_summary_value = item['moisture']

    return (
        f"## {emoji} {comment['content']} {emoji}\n"
        f"Rarity: **{comment['rarity']}**\n"
        f"### 24h Average Moisture: **{average}%**\n"
        f"Summary:\n{summary_lines}"
    )


def create_teams_card(daily_data: List[Dict[str, int]]):
    if not daily_data:
        return {
            "type": "message",
            "attachments": [{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {"type": "TextBlock", "text": "No data from the last 24 hours.", "weight": "Bolder"}
                    ]
                }
            }]
        }

    avg = round(sum(item["moisture"] for item in daily_data) / len(daily_data))

    # your existing buckets
    if avg < 20:
        comment = random_from_list(comments.very_dry)
        emoji = random_from_list(emojis.dry)
    elif avg < 40:
        comment = random_from_list(comments.dry)
        emoji = random_from_list(emojis.dry)
    elif avg < 60:
        comment = random_from_list(comments.ok)
        emoji = random_from_list(emojis.ok)
    elif avg < 80:
        comment = random_from_list(comments.wet)
        emoji = random_from_list(emojis.wet)
    else:
        comment = random_from_list(comments.very_wet)
        emoji = random_from_list(emojis.wet)

    # build summary lines every 3 hours
    summary_lines = []
    prev = daily_data[0]["moisture"]
    for item in daily_data:
        if item["hour"] % 3 == 0 and item["hour"] != 0:
            hour = item["hour"]
            hour_emoji = "🕛 " if hour in (12, 24) else "🕒 " if hour in (3, 15) else "🕕 " if hour in (6, 18) else "🕘 " if hour in (9, 21) else ""
            change_emoji = "🔼" if item["moisture"] > prev else "🔽" if item["moisture"] < prev else "➖"
            summary_lines.append(f"- {hour_emoji}{hour:02d} - {item['moisture']}% {change_emoji}")
            prev = item["moisture"]

    # Adaptive Card
    card = {
        "type": "message",
        "attachments": [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.4",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": f"{emoji} {comment['content']} {emoji}",
                        "wrap": True,
                        "size": "Large",
                        "weight": "Bolder"
                    },
                    {
                        "type": "FactSet",
                        "facts": [
                            {"title": "Rarity", "value": str(comment['rarity'])},
                            {"title": "24h Avg Moisture", "value": f"{avg}%"}
                        ]
                    },
                    {
                        "type": "TextBlock",
                        "text": "**Summary (every 3h):**",
                        "wrap": True,
                        "spacing": "Medium"
                    },
                    {
                        "type": "TextBlock",
                        "text": "\n".join(summary_lines) if summary_lines else "_No checkpoints_",
                        "wrap": True
                    }
                ]
            }
        }]
    }
    return card
