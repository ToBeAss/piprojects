import math
import random
from aloe.personality import comments, emojis

def random_from_list(array):
    return array[math.floor(random.random() * len(array))]

def create_message(percentage: int):
    if percentage is None:
        return "I'm not able to read data from the sensor at the moment."
    
    if percentage < 20:
        comment = random_from_list(comments.very_dry)
        emoji = random_from_list(emojis.dry)
    elif percentage < 40:
        comment = random_from_list(comments.dry)
        emoji = random_from_list(emojis.dry)
    elif percentage < 60:
        comment = random_from_list(comments.ok)
        emoji = random_from_list(emojis.ok)
    elif percentage < 80:
        comment = random_from_list(comments.wet)
        emoji = random_from_list(emojis.wet)
    else:
        comment = random_from_list(comments.very_wet)
        emoji = random_from_list(emojis.wet)

    return (
        f"### {comment['content']}\n"
        f"Rarity: **{comment['rarity']}**\n"
        f"Moisture Level: **{percentage}%**\n"
        f"### {emoji}"
    )