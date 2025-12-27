# This modules provides access to Motherduck and its persistent data (ohlcv and exchange tickers)
import os

import duckdb
from dotenv import load_dotenv

load_dotenv()


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

        self.conn.execute(
            """
            INSERT INTO trades (
            execution_id,
            created_at,
            filled_at,
            filled_avg_price,
            filled_qty,
            position_intent,
            side,
            symbol,
            is_paper,
            order_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            [
                data.execution_id,
                data.order.created_at,
                data.order.filled_at,
                float(data.order.filled_avg_price)
                if data.order.filled_avg_price
                else None,
                float(data.order.filled_qty) if data.order.filled_qty else None,
                data.order.position_intent.value
                if data.order.position_intent
                else None,
                data.order.side.value,
                data.order.symbol,
                is_paper,
                data.order.id,
            ],
        )
