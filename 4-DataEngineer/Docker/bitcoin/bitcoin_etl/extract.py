
import requests
import polars as pl
import logging
from datetime import datetime, timedelta, timezone
import random
import time

logger = logging.getLogger(__name__)

def generate_mock_data():
    """
    Generate mock Bitcoin price data when the API is not available
    
    Returns:
        Polars DataFrame with simulated price data
    """
    logger.warning("Generating mock data as API is not available")
    
    # Current timestamp
    now = datetime.now(timezone.utc)
    
    # Base price (around current Bitcoin price)
    base_price = 65000 + random.uniform(-2000, 2000)
    
    # Exchanges to simulate
    exchanges = ["Binance", "Coinbase", "Kraken", "Bitstamp", "Bitfinex", "Gemini", "Huobi"]
    
    # Create mock data
    mock_tickers = []
    
    for exchange in exchanges:
        # Add some variation to prices for different exchanges
        exchange_factor = 0.98 + (hash(exchange) % 5) / 100  # Variation between 0.98 and 1.02
        price = base_price * exchange_factor
        
        # Add some random noise to the price
        price += random.uniform(-100, 100)
        
        # Generate random volume
        volume = random.uniform(10, 100) * 1000
        
        # Add some time variation (within the last 10 minutes)
        time_offset = random.randint(0, 600)  # seconds
        timestamp = now - timedelta(seconds=time_offset)
        
        mock_tickers.append({
            "exchange": exchange,
            "price": price,
            "volume": volume,
            "timestamp": timestamp,
            "pair": "BTC/USD",
            "trust_score": "green"
        })
    
    return pl.DataFrame(mock_tickers)

def extract_bitcoin_data(config):
    """
    Extract Bitcoin price data from the CoinGecko tickers API in real-time
    with fallback to mock data if API is unavailable
    
    Args:
        config: Configuration dictionary containing API parameters
        
    Returns:
        Polars DataFrame with raw price data
    """
    # Use the tickers API for real-time data
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/tickers"
    
    # Get retry configuration
    max_retries = int(config.get("max_retries", 3))
    retry_delay = int(config.get("retry_delay", 2))
    use_mock_on_failure = config.get("use_mock_on_failure", "true").lower() == "true"
    
    # Try to get data from API with retries
    for attempt in range(max_retries):
        try:
            logger.info(f"Fetching real-time data from {url} (attempt {attempt+1}/{max_retries})")
            response = requests.get(url, timeout=10)  # Add timeout
            response.raise_for_status()
            
            data = response.json()
            
            # Extract tickers data
            tickers = data.get("tickers", [])
            if not tickers:
                logger.warning("No tickers data returned from API")
                if use_mock_on_failure:
                    return generate_mock_data()
                return pl.DataFrame()
            
            # Create a list to store processed ticker data
            processed_tickers = []
            
            # Process each ticker
            for ticker in tickers:
                # Only include tickers with USD or USDT as target
                if ticker["target"] in ["USD", "USDT"]:
                    # Parse the timestamp with timezone information
                    try:
                        # Try to parse with timezone
                        timestamp = datetime.strptime(ticker["last_traded_at"], "%Y-%m-%dT%H:%M:%S%z")
                    except ValueError:
                        try:
                            # Try to parse with timezone in a different format
                            timestamp = datetime.strptime(ticker["last_traded_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                        except ValueError:
                            # If timezone parsing fails, use UTC
                            timestamp_str = ticker["last_traded_at"].split('+')[0].split('Z')[0]
                            if '.' in timestamp_str:
                                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc)
                            else:
                                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
                    
                    processed_tickers.append({
                        "exchange": ticker["market"]["name"],
                        "price": ticker["last"],
                        "volume": ticker["volume"],
                        "timestamp": timestamp,
                        "pair": f"{ticker['base']}/{ticker['target']}",
                        "trust_score": ticker.get("trust_score", "unknown")
                    })
            
            # Convert to Polars DataFrame
            if not processed_tickers:
                logger.warning("No USD/USDT tickers found")
                if use_mock_on_failure:
                    return generate_mock_data()
                return pl.DataFrame()
                
            df = pl.DataFrame(processed_tickers)
            
            logger.info(f"Successfully extracted {len(df)} ticker records in real-time")
            return df
            
        except (requests.RequestException, requests.Timeout) as e:
            logger.warning(f"API request failed (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to fetch data from API after {max_retries} attempts: {e}")
                if use_mock_on_failure:
                    return generate_mock_data()
                raise
        except Exception as e:
            logger.error(f"Error processing ticker data: {e}")
            if use_mock_on_failure:
                return generate_mock_data()
            raise
