from pathlib import Path
import duckdb


# Project locations
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"
DB_PATH = PROJECT_ROOT / "warehouse.duckdb"


# Connect to DuckDB
con = duckdb.connect(str(DB_PATH))


# Create raw schema
con.execute("CREATE SCHEMA IF NOT EXISTS raw")


# Source CSV files → DuckDB table names
tables = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}


for table_name, filename in tables.items():

    csv_path = DATA_DIR / filename

    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {csv_path}"
        )

    print(f"Loading {filename} → raw.{table_name}")

    con.execute(
        f"""
        CREATE OR REPLACE TABLE raw.{table_name} AS
        SELECT *
        FROM read_csv_auto(
            '{csv_path.as_posix()}',
            header = true
        );
        """
    )


print("\nRaw tables created successfully.\n")

# Show table row counts
for table_name in tables:
    count = con.execute(
        f"SELECT COUNT(*) FROM raw.{table_name}"
    ).fetchone()[0]

    print(f"raw.{table_name:<20} {count:,} rows")


con.close()