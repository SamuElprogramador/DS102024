import os
import logging
from sqlalchemy import create_engine, text
from datetime import date, datetime, timedelta
import polars as pl

logger = logging.getLogger(__name__)

def get_last_processed_date(config):
    """
    Get the last processed timestamp from the database
    
    Args:
        config: Configuration dictionary with database info
        
    Returns:
        datetime: The last processed timestamp or None if no data exists
    """
    database_url = os.getenv("DATABASE_URL")
    schema = config["schema"]
    table = config["table"]
    full_table_name = f"{schema}.{table}"
    
    # Create SQLAlchemy engine
    engine = create_engine(database_url)
    
    try:
        # Query the last timestamp
        with engine.connect() as conn:
            query = text(f"SELECT MAX(minute_timestamp) FROM {full_table_name}")
            result = conn.execute(query).scalar()
            
        if result:
            logger.info(f"Last processed timestamp found: {result}")
            return result
        else:
            logger.info("No previous data found in the database")
            return None
    except Exception as e:
        logger.error(f"Failed to query last processed timestamp: {e}")
        return None
    finally:
        engine.dispose()

def load_to_postgres(df, config):
    """
    Load transformed data to PostgreSQL
    
    Args:
        df: Polars DataFrame with transformed data
        config: Configuration dictionary with database info
    """
    if df.is_empty():
        logger.warning("No data to load to database")
        return
    
    database_url = os.getenv("DATABASE_URL")
    schema = config["schema"]
    table = config["table"]
    full_table_name = f"{schema}.{table}"
    
    # Convert Polars DataFrame to Pandas for SQLAlchemy compatibility
    pandas_df = df.to_pandas()
    
    # Create SQLAlchemy engine
    engine = create_engine(database_url)
    
    try:
        # Check for duplicate timestamps and handle them
        with engine.connect() as conn:
            # Get list of timestamps in the current batch
            timestamps_list = ", ".join([f"'{ts}'" for ts in pandas_df['minute_timestamp'].astype(str).tolist()])
            if timestamps_list:
                # Delete any existing records with the same timestamps to avoid duplicates
                delete_query = text(f"DELETE FROM {full_table_name} WHERE minute_timestamp IN ({timestamps_list})")
                conn.execute(delete_query)
                conn.commit()
                logger.info(f"Removed any existing records for the timestamps being processed")
        
        # Load data to PostgreSQL
        logger.info(f"Loading {len(df)} records to {full_table_name}")
        pandas_df.to_sql(
            table,
            engine,
            schema=schema,
            if_exists="append",
            index=False
        )
        logger.info(f"Successfully loaded data to {full_table_name}")
    except Exception as e:
        logger.error(f"Failed to load data to database: {e}")
        raise
    finally:
        engine.dispose()