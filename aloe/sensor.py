import csv
from datetime import datetime
import math

try:
    import spidev
except ImportError:
    print("spidev library not installed. Please install it using 'pip install spidev'.")
    spidev = None


# Sensor calibration values
DRY = 700
WET = 800

# File paths
DATA_FOLDER = "aloe/data/"  # aloe/data/
DATA_FILE = "readings.csv"
SUMMARY_FILE = "hourly_summary.csv"


def read_sensor():
    # Check if spidev was successfully imported
    if spidev is None:
        print("spidev is not available. Exiting read_sensor function.")
        return None
    
    spi = None
    try:
        # Initialize SPI
        spi = spidev.SpiDev()
        spi.open(0, 0) # Open SPI bus 0, device (CS) 0
        spi.max_speed_hz = 1350000 # Set SPI clock speed

        # Read ADC data
        adc = spi.xfer2([1, (8 + 0) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]

        return data
    except Exception as e:
        print(f"Error reading sensor: {e}")
        return None
    finally:
        # CRITICAL: Always close the SPI connection to prevent "Too many open files"
        if spi is not None:
            try:
                spi.close()
            except:
                pass

def map(raw_data: int):
    # Return percentage
    return max(0, min(100, int((raw_data - DRY) * 100 / (WET - DRY))))


def get_data():
    raw_data = read_sensor()
    if raw_data is None:
        return None  # Return None if sensor reading failed
        
    return {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), 
        "Moisture": raw_data, 
        "Moisture(%)": map(raw_data)
    }

def get_summary(temp: list[int]):
    if not temp or len(temp) == 0:
        # Return default values if no data
        return {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:00"),
            "Avg Moisture" : 0, 
            "Avg Moisture(%)" : 0, 
            "Median Moisture" : 0, 
            "Median Moisture(%)" : 0, 
            "Min Moisture" : 0, 
            "Min Moisture(%)" : 0, 
            "Max Moisture" : 0, 
            "Max Moisture(%)" : 0
        }
    
    temp_copy = temp.copy()  # Don't modify the original list
    temp_copy.sort()
    mid = math.floor((len(temp_copy)-1)/2)

    _min = min(temp_copy)
    _max = max(temp_copy)
    _avg = sum(temp_copy) / len(temp_copy)
    _med = temp_copy[mid]

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
    try:
        with open(path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            # Write header if file is new
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(row)
    except Exception as e:
        print(f"Error writing to CSV {path}: {e}")
        # Could send Discord notification here for file system issues
        raise  # Re-raise to let caller handle
