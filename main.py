import scripts.timeout as timeout
import aloe.main as aloe
import scripts.discord as discord
import data.webhooks as webhooks

def main():
    # Test function
    discord.send_to_discord(webhooks.aloe, "Hello World!")
    while True:
        # Wait until next whole hour before running the rest of the program
        timeout.next_hour()

        # Run projects
        aloe.main()

main()
