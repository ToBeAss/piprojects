# Aloe Plant Monitor 🌱

An IoT soil moisture monitoring system for my aloe plant, hosted on a Raspberry Pi Zero WH. The system reads soil moisture levels every minute and sends personalized Discord messages with the plant's "personality" based on its hydration needs.

## Features ✨

- **Real-time Monitoring**: Reads soil moisture every minute using an analog sensor via SPI
- **Plant Personality**: The plant communicates through Discord with different moods and comments based on moisture levels
- **Data Collection**: Stores both raw readings and hourly summaries in CSV format
- **Automated Updates**: Daily Discord reports at midnight with 24-hour moisture averages
- **Auto-deployment**: Automatic git pulls and service restarts when code changes are detected
- **Rarity System**: Comments have different rarity levels (Common, Uncommon, Rare) for variety

## Hardware Setup 🔧

### Required Components:
- Raspberry Pi Zero WH
- Analog soil moisture sensor
- MCP3008 ADC (Analog-to-Digital Converter)
- Jumper wires
- Breadboard (optional)

### Wiring:
The soil moisture sensor connects to the Raspberry Pi via SPI through an MCP3008 ADC:
- Sensor analog output → MCP3008 CH0
- MCP3008 → Raspberry Pi SPI pins

## Software Requirements 📋

- Python 3.x
- Required packages (install with `pip install -r requirements.txt`):
  - `spidev` - For SPI communication
  - `requests` - For Discord webhook integration

## Installation 🚀

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ToBeAss/piprojects.git
   cd piprojects
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Discord webhooks**:
   - Create Discord webhooks for your channels
   - Update `my_secrets/webhooks.py` with your webhook URLs

4. **Configure sensor calibration**:
   - Adjust `DRY` and `WET` values in `aloe/sensor.py` based on your sensor
   - Test in completely dry soil and fully saturated soil

5. **Set up as a system service** (optional):
   ```bash
   sudo systemctl enable myscript.service
   sudo systemctl start myscript.service
   ```

6. **Enable auto-deployment** (optional):
   - Set up a cron job to run `auto_pull_and_restart.sh` periodically
   - Automatically pulls updates from GitHub and restarts the service

## How It Works 🔄

1. **Minute-by-minute**: Collects soil moisture data every minute
2. **Hourly summaries**: At the top of each hour, calculates median moisture and stores summary
3. **Daily reports**: At midnight, sends a Discord message with personality-based comments and emojis
4. **Continuous monitoring**: Runs 24/7, storing all data in CSV files for later analysis

## Plant Personality System 😄

The aloe plant has different moods based on soil moisture levels:

- **Very Dry (< 20%)**: Desperate, dramatic comments 🏜️
- **Dry (20-40%)**: Polite requests for water 🌵
- **Just Right (40-60%)**: Content and happy 😊
- **Wet (60-80%)**: Grateful but getting concerned 💧
- **Very Wet (> 80%)**: Worried about overwatering ☔

Each category has multiple comment variations with different rarity levels to keep interactions fresh and entertaining!

## File Structure 📁

```
piprojects/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── auto_pull_and_restart.sh  # Auto-deployment script
├── aloe/                      # Plant-specific modules
│   ├── sensor.py             # Sensor reading and data storage
│   ├── message.py            # Discord message generation
│   ├── data/                 # CSV data storage
│   └── personality/          # Plant personality system
│       ├── comments.py       # Mood-based comments
│       └── emojis.py         # Matching emojis
├── src/                      # General utilities
│   ├── discord.py           # Discord webhook integration
│   └── timeout.py           # Timing utilities
└── my_secrets/              # Private configuration
    └── webhooks.py          # Discord webhook URLs
```

## Data Storage 💾

- **readings.csv**: Raw sensor data with timestamps
- **hourly_summary.csv**: Hourly moisture summaries and statistics

## Contributing 🤝

Feel free to fork this project and adapt it for your own plants! Ideas for improvements:
- Support for multiple sensors/plants
- Web dashboard for data visualization
- Mobile app notifications
- Integration with home automation systems

## License 📄

This project is open source - feel free to use and modify as needed!

---

*Made with ❤️ for my thirsty aloe plant*
