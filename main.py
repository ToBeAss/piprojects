import scripts.timeout as timeout
import aloe.main as aloe
import scripts.discord as discord
import my_secrets.webhooks as webhooks

def main():
    # When the Raspberry Pi is rebooted, it should automatically start the main script an display this message:
    discord.send_to_discord(webhooks.aloe, "System rebooted")
    
    while True:
        # Wait until next whole hour before running the rest of the program
        timeout.next_hour()

        # Run projects
        aloe.main()

main()