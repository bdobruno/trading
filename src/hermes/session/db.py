# This modules provides access to Motherduck and its persistent data (ohlcv and exchange tickers)
import os

import duckdb


class DuckDBConnector:
    def __init__(self, db_path: str = "md:stocksdb"):
        self.db_path = db_path
        self._setup_motherduck_token()
        self.conn = duckdb.connect(self.db_path)

    def _setup_motherduck_token(self) -> None:
        """Set up MotherDuck token if available."""
        token = os.getenv("MOTHERDUCK_TOKEN")
        if token:
            os.environ["motherduck_token"] = token

    def log_trades(self, data, is_paper: bool) -> None:
        """
        Add trades to the database.
        """

        self.conn.execute("""
            INSERT INTO trades (
            order_id, 
            created_at, 
            filled_at, 
            filled_avg_price,
            filled_qty,
            position_intent,
            side,
            symbol,
            is_paper
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            data.id,
            data.created_at,
            data.filled_at,
            float(data.filled_avg_price) if data.filled_avg_price else None,
            float(data.filled_qty) if data.filled_qty else None,
            data.position_intent.value if data.position_intent else None,
            data.side.value,
            data.symbol,
            is_paper
        ])
