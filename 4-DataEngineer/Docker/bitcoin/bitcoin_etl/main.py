import logging
import configparser
from pathlib import Path
import os
from datetime import datetime, timedelta, timezone
import traceback

import polars as pl
from dotenv import load_dotenv

from bitcoin_etl.extract import extract_bitcoin_data
from bitcoin_etl.transform import transform_data
from bitcoin_etl.load import load_to_postgres, get_last_processed_date
from bitcoin_etl.models import setup_database

# Set up logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    try:
        # Load configuration
        config = configparser.ConfigParser()
        config.read(Path(__file__).parent.parent / "config.ini")
        
        logger.info("Starting Bitcoin ETL process for real-time data")
        
        # Set up database
        logger.info("Setting up database")
        setup_database()
        
        # Get last processed timestamp
        last_timestamp = get_last_processed_date(config["database"])
        
        # Extract data
        logger.info(f"Extracting Bitcoin price data in real-time")
        raw_data = extract_bitcoin_data(config["api"])
        
        if raw_data.is_empty():
            logger.info("No data extracted. Exiting.")
            return
        
        # Transform data
        logger.info("Transforming data with minute-level granularity")
        transformed_data = transform_data(raw_data)
        
        # Filter out already processed timestamps if needed
        if last_timestamp:
            logger.info(f"Filtering out data before {last_timestamp}")
            # Convert last_timestamp to string for comparison to avoid timezone issues
            last_timestamp_str = last_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            # Use string comparison to avoid timezone issues
            transformed_data = transformed_data.with_columns(
                pl.col("minute_timestamp").dt.strftime("%Y-%m-%d %H:%M:%S").alias("timestamp_str")
            ).filter(
                pl.col("timestamp_str") > last_timestamp_str
            ).drop("timestamp_str")
            
        if transformed_data.is_empty():
            logger.info("No new data to load after filtering. Exiting.")
            return
            
        logger.info(f"Loading {len(transformed_data)} new records to PostgreSQL")
        
        # Load data to PostgreSQL
        load_to_postgres(transformed_data, config["database"])
        
        logger.info("Real-time ETL process completed successfully")
    except Exception as e:
        logger.error(f"Error in ETL process: {e}")
        logger.error(traceback.format_exc())
        # Don't re-raise the exception to allow the scheduler to continue

if __name__ == "__main__":
    main()