
import configparser
from bitcoin_etl.extract import extract_bitcoin_data

# Load configuration
config = configparser.ConfigParser()
config.read("config.ini")

# Extract data
print("Extracting Bitcoin ticker data...")
data = extract_bitcoin_data(config["api"])

# Display data
if not data.is_empty():
    print(f"Successfully extracted {len(data)} records")
    print("Sample data:")
    print(data.head(5))
else:
    print("No data extracted")
