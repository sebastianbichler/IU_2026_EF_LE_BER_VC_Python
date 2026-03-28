import dask.dataframe as dd
import pandas as pd

def ingest_csv(path: str):
    return dd.read_csv(path, parse_dates=["shipped_at","delivered_at"], assume_missing=True)

def transform_basic(ddf):

    ddf["status"] = ddf["status"].str.lower()

    ddf = ddf[ddf["weight_kg"] >= 0]

    def add_transit(df: pd.DataFrame):
        df = df.copy()
        df["transit_hours"] = (
            (df["delivered_at"] - df["shipped_at"])
            .dt.total_seconds() / 3600
        )
        return df

    ddf = ddf.map_partitions(add_transit)

    ddf["route_id"] = ddf["origin"].str.upper() + "-" + ddf["destination"].str.upper()

    return ddf

def aggregate_stats(ddf):
    stats = (
        ddf.groupby("route_id")
        .agg({
            "parcel_id":"count",
            "weight_kg":"mean",
            "transit_hours":"mean"
        })
        .rename(columns={
            "parcel_id":"count",
            "weight_kg":"avg_weight",
            "transit_hours":"avg_transit"
        })
    )

    return stats.reset_index()

def run_pipeline(input_path, output_path):

    ddf = ingest_csv(input_path)
    ddf = transform_basic(ddf)

    stats = aggregate_stats(ddf)

    ddf.to_parquet(output_path, write_index=False, partition_on=["status"])

    stats.compute().to_parquet(output_path + "_stats.parquet")