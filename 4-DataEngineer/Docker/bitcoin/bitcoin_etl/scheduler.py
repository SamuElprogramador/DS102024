import schedule
import time
import logging
import subprocess
import os
import configparser
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def run_etl_job():
    """Run the ETL process as a subprocess"""
    logger.info("Starting scheduled ETL job")
    try:
        result = subprocess.run(
            ["python", "-m", "bitcoin_etl.main"],
            check=True,
            capture_output=True,
            text=True,
            timeout=60  # Add timeout to prevent hanging jobs
        )
        logger.info(f"ETL job completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"ETL job failed with error:\n{e.stderr}")
    except subprocess.TimeoutExpired:
        logger.error("ETL job timed out after 60 seconds")
    except Exception as e:
        logger.error(f"Unexpected error running ETL job: {e}")

def main():
    """Set up the scheduler"""
    # Load configuration
    config = configparser.ConfigParser()
    config.read(Path(__file__).parent.parent / "config.ini")
    
    # Get schedule frequency from config
    schedule_freq = config.get("etl", "schedule", fallback="daily")
    
    if schedule_freq == "daily":
        logger.info("Configuring ETL job to run daily at midnight")
        schedule.every().day.at("00:00").do(run_etl_job)
    elif schedule_freq == "2min":
        logger.info("Configuring ETL job to run every 2 minutes")
        schedule.every(2).minutes.do(run_etl_job)
    else:
        logger.info(f"Unrecognized schedule '{schedule_freq}', defaulting to every 2 minutes")
        schedule.every(2).minutes.do(run_etl_job)
    
    logger.info(f"Scheduler started. ETL job will run according to schedule: {schedule_freq}")
    
    # Run the job immediately on startup
    run_etl_job()
    
    # Keep the scheduler running
    while True:
        try:
            schedule.run_pending()
            time.sleep(10)  # Check every 10 seconds for pending jobs
        except Exception as e:
            logger.error(f"Error in scheduler: {e}")
            # Continue running even if there's an error
            time.sleep(30)  # Wait a bit longer after an error

if __name__ == "__main__":
    main()