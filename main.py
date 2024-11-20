import src.timeout as timeout
import src.discord as discord
import my_secrets.webhooks as webhooks

import aloe.sensor as sensor
import aloe.message as message

def main():
    # When the Raspberry Pi is rebooted, it should automatically start the main script an display this message:
    discord.send_to_discord(webhooks.aloe, "System rebooted")

    temp = [] # Temporary readings deleted every hour
    
    while True:
        # Wait until next whole hour before running the rest of the program
        next_hour = timeout.next_hour()
        next_min = timeout.next_min()

        if (next_hour <= next_min):
            # Calculate a summary every hour and send the result to Discord
            timeout.sleep(next_hour)
            summary = sensor.get_summary(temp)
            sensor.store_summary(summary)
            result = summary["Median Moisture(%)"]
            content = message.create_message(result)
            discord.send_to_discord(webhooks.aloe, content)
            temp = []
            data = sensor.get_data()
            temp.append(data["Moisture"])
            sensor.store_data(data)
        else:
            # Read sensor data every minute
            timeout.sleep(next_min)
            data = sensor.get_data()
            temp.append(data["Moisture"])
            sensor.store_data(data)

main()
