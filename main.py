import scripts.timeout as timeout
import aloe.main as aloe

def main():
    while True:
        # Wait until next whole hour before running the rest of the program
        timeout.next_hour()

        # Run projects
        aloe.main()

main()
