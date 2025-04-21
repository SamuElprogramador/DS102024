# pip install "polars[database]" connectorx psycopg2-binary

import polars as pl

uri   = "postgresql://user:password@localhost:6543/bitcoin"
query = "SELECT * FROM bitcoin.prices ORDER BY date DESC LIMIT 100"

df = pl.read_database_uri(query, uri, engine="connectorx")   # o engine="adbc"
print(df.head())
