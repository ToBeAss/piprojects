import math
import random
from aloe.data import comments, emojis

def random_from_list(array):
    return array[math.floor(random.random() * len(array))]

def create_message(reading: int):
    if reading < 33.33:
        comment = random_from_list(comments.dry)
        emoji = random_from_list(emojis.dry)
    elif reading < 66.67:
        comment = random_from_list(comments.ok)
        emoji = random_from_list(emojis.ok)
    else:
        comment = random_from_list(comments.wet)
        emoji = random_from_list(emojis.wet)

    return f"{comment}\nMoisture Level: **{reading}%**\n{emoji}"