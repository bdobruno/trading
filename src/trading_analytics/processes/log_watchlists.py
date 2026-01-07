import json

import polars as pl

from trading_analytics.db.db import DuckDBConnector


def to_df(tickers: list[str], event_type: str = "add") -> pl.DataFrame:
    return pl.DataFrame({"ticker": tickers, "event_type": event_type}).filter(
        pl.col("ticker") != ""
    )


def main():
    data = json.load(open("src/trading_analytics/processes/watchlist.json"))
    pets = data["pets"]
    gappers = data["gappers"]
    with DuckDBConnector() as db:
        if pets:
            print("Logging pets")
            pets_df = to_df(pets)
            db.add_tickers(pets_df, type="pets")
            print("Pets in DB")
        if gappers:
            print("Logging gappers")
            gappers_df = to_df(gappers)
            db.add_tickers(gappers_df, type="gappers")
            print("Gappers in DB")


if __name__ == "__main__":
    main()
