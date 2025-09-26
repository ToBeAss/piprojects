from datetime import datetime
import src.reboot as reboot
import src.timeout as timeout
import src.discord as discord
import src.teams as teams
import my_secrets.webhooks as webhooks

import aloe.sensor as sensor
import aloe.message as message

def main():
    try:
        reboot.announce_reboot(webhooks.piprojects, iface="wlan0")
    except Exception as e:
        print(f"Failed to send reboot message: {e}")
    
    hourly_data = []
    daily_data = []
    last_hour_sent = None

    while True:
        try:
            # Always sleep to next whole minute
            timeout.sleep_until(timeout.next_min())
            now = datetime.now()

            # 1) read once per minute
            data = sensor.get_data()
            if data and data.get("Moisture") is not None:
                sensor.store_data(data)
                hourly_data.append(data["Moisture"])
            else:
                print(f"[WARN] {now:%H:%M:%S} failed to read sensor")

            # 2) once per hour (idempotent guard)
            if now.minute == 0 and now.hour != last_hour_sent:
                if hourly_data:
                    summary = sensor.get_summary(hourly_data)
                    sensor.store_summary(summary)
                    median_pct = summary["Median Moisture(%)"]
                    hour = now.hour

                    # visibility: always tell Discord what we're about to do
                    try:
                        discord.send_to_discord(
                            webhooks.piprojects,
                            f"[DEBUG] {now:%Y-%m-%d %H:%M:%S} hour={hour} samples={len(hourly_data)} median%={median_pct} (will_send_to_teams={8 <= hour <= 16})"
                        )
                    except Exception: pass

                    if 8 <= hour <= 16:
                        content = message.create_teams_message(median_pct)
                        mode, status, err = teams.send_to_teams(webhooks.kvteams, content)
                        # mirror outcome to Discord so you can see it remotely
                        try:
                            discord.send_to_discord(
                                webhooks.piprojects,
                                f"[DEBUG] Teams send: mode={mode} status={status} err={err or 'None'} at {hour:02d}:00"
                            )
                        except Exception: pass

                    # daily rollup window
                    daily_hour = 24 if hour == 0 else hour
                    daily_data.append({"hour": daily_hour, "moisture": median_pct})

                    # reset AFTER processing
                    hourly_data = []
                else:
                    try:
                        discord.send_to_discord(
                            webhooks.piprojects,
                            f"[WARN] {now:%Y-%m-%d %H:%M:%S} no samples collected during hour={now.hour}; skipping Teams send"
                        )
                    except Exception: pass

                last_hour_sent = now.hour

            # 3) midnight Discord daily (unchanged)
            if now.hour == 0 and now.minute == 0:
                if len(daily_data) > 0:
                    content = message.create_message(daily_data)
                    try:
                        discord.send_to_discord(webhooks.aloe, content)
                    except Exception as e:
                        try:
                            discord.send_to_discord(webhooks.piprojects, f"[ERROR] daily Discord send failed: {e}")
                        except Exception: pass
                    daily_data = []
                    daily_data.append({"hour": 0, "moisture": summary["Median Moisture(%)"]})
                
        except Exception as e:
            try:
                discord.send_to_discord(webhooks.piprojects, f"[ERROR] main loop: {e}")
            except Exception: pass

main()
