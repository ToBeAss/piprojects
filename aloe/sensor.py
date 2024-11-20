import csv
from datetime import datetime
import math

try:
    import spidev
except ImportError:
    print("spidev library not installed. Please install it using 'pip install spidev'.")
    spidev = None


# Sensor calibration values
DRY = 750
WET = 850

# File paths
DATA_FOLDER = "aloe/data/"
DATA_FILE = "readings.csv"
SUMMARY_FILE = "hourly_summary.csv"

# Temporary readings
temp = []


def read_sensor():
    # Check if spidev was successfully imported
    if spidev is None:
        print("spidev is not available. Exiting read_sensor function.")
        return 800 #None
    
    # Initialize SPI
    spi = spidev.SpiDev()
    spi.open(0, 0) # Open SPI bus 0, device (CS) 0
    spi.max_speed_hz = 1350000 # Set SPI clock speed

    # Read ADC data
    adc = spi.xfer2([1, (8 + 0) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]

    # Return raw data
    return data

def map(raw_data: int):
    # Return percentage
    return max(0, min(100, int((raw_data - DRY) * 100 / (WET - DRY))))


def get_data():
    global temp
    data = read_sensor()
    temp.append(data) # Temporarily stores raw data to array
    return {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
        "Moisture": data, 
        "Moisture(%)": map(data)
    }

def get_summary():
    global temp
    temp.sort()
    mid = math.floor((len(temp)-1)/2)

    _min = min(temp)
    _max = max(temp)
    _avg = sum(temp) / len(temp)
    _med = temp[mid]

    temp = [] # Clear temporary data every hour
    return {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:00"),
        "Avg Moisture" : _avg, 
        "Avg Moisture(%)" : map(_avg), 
        "Median Moisture" : _med, 
        "Median Moisture(%)" : map(_med), 
        "Min Moisture" : _min, 
        "Min Moisture(%)" : map(_min), 
        "Max Moisture" : _max, 
        "Max Moisture(%)" : map(_max)
    }
    

def store_data(data: object):
    path = DATA_FOLDER + DATA_FILE
    fieldnames = ["Timestamp", "Moisture", "Moisture(%)"]
    write_to_csv(path, fieldnames, data)

def store_summary(summary: object):
    path = DATA_FOLDER + SUMMARY_FILE
    fieldnames = ["Timestamp", "Avg Moisture", "Avg Moisture(%)", "Median Moisture", "Median Moisture(%)", "Min Moisture", "Min Moisture(%)", "Max Moisture", "Max Moisture(%)"]
    write_to_csv(path, fieldnames, summary)

def write_to_csv(path: str, fieldnames: list[str], row: object):
    with open(path, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Write header if file is new
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(row)