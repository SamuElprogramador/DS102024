import polars as pl
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def transform_data(df):
    """
    Transform the raw Bitcoin ticker data with minute-level granularity
    
    Args:
        df: Polars DataFrame with raw ticker data
        
    Returns:
        Transformed Polars DataFrame
    """
    if df.is_empty():
        logger.warning("Empty DataFrame received for transformation")
        return df
    
    logger.info("Starting data transformation with minute-level granularity")
    
    # Extract date and datetime with minute precision for grouping
    transformed_df = (
        df.with_columns([
            pl.col("timestamp").dt.date().alias("date"),
            # Truncate timestamp to minute precision and ensure UTC timezone
            pl.col("timestamp").dt.truncate("1m").alias("minute_timestamp")
        ])
    )
    
    # Calculate metrics by minute across all exchanges
    minute_df = (
        transformed_df.group_by("minute_timestamp")
        .agg([
            pl.col("price").min().alias("min_price"),
            pl.col("price").max().alias("max_price"),
            # Volume-weighted average price
            ((pl.col("price") * pl.col("volume")).sum() / pl.col("volume").sum()).alias("avg_price"),
            pl.col("price").first().alias("open_price"),
            pl.col("price").last().alias("close_price"),
            pl.col("volume").sum().alias("total_volume"),
            pl.col("exchange").n_unique().alias("exchange_count")
        ])
        .with_columns([
            # Extract date from minute_timestamp for database storage
            pl.col("minute_timestamp").dt.date().alias("date"),
            # Calculate price changes
            (pl.col("close_price") - pl.col("open_price")).alias("price_change"),
            ((pl.col("close_price") - pl.col("open_price")) / pl.col("open_price") * 100).alias("price_change_pct")
        ])
        .sort("minute_timestamp")
    )
    
    logger.info(f"Transformation complete. Transformed {len(minute_df)} minute-level records")
    return minute_df