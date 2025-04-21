from sqlalchemy import create_engine, Column, Integer, Float, Date, DateTime, text, Identity
from sqlalchemy.ext.declarative import declarative_base
import os
import logging
import time

logger = logging.getLogger(__name__)

Base = declarative_base()

class BitcoinPrice(Base):
    """SQLAlchemy model for Bitcoin price data with minute-level granularity"""
    __tablename__ = 'prices'
    __table_args__ = {'schema': 'bitcoin'}
    
    id = Column(Integer, Identity(always=True), primary_key=True)
    date = Column(Date, nullable=False, index=True)
    minute_timestamp = Column(DateTime, nullable=False, index=True, unique=True)
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    avg_price = Column(Float, nullable=False)
    open_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    price_change = Column(Float, nullable=False)
    price_change_pct = Column(Float, nullable=False)
    total_volume = Column(Float, nullable=False)
    exchange_count = Column(Integer, nullable=False)

def setup_database(max_retries=5, retry_interval=10):
    """
    Set up the PostgreSQL database and schema with retry mechanism
    
    Args:
        max_retries: Maximum number of connection attempts
        retry_interval: Seconds to wait between retries
    """
    database_url = os.getenv("DATABASE_URL")
    retries = 0
    
    while retries < max_retries:
        try:
            logger.info(f"Attempting to connect to database (attempt {retries + 1}/{max_retries})")
            engine = create_engine(database_url)
            
            # Test connection
            engine.connect().close()
            
            # Create schema if it doesn't exist
            with engine.connect() as conn:
                conn.execute(text("CREATE SCHEMA IF NOT EXISTS bitcoin"))
                conn.commit()
            
            # Create tables
            Base.metadata.create_all(engine)
            logger.info("Database setup completed successfully")
            return
        except Exception as e:
            retries += 1
            if retries >= max_retries:
                logger.error(f"Failed to set up database after {max_retries} attempts: {e}")
                raise
            else:
                logger.warning(f"Database connection failed: {e}. Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)