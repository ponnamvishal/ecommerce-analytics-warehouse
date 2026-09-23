import duckdb

DB_PATH = r"C:\Users\VISHAL\ecommerce-analytics-warehouse\warehouse.duckdb"

with duckdb.connect(DB_PATH) as con:
    rows = con.execute("""
        SELECT
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'intermediate'
          AND table_name = 'int_order_items_enriched'
        ORDER BY ordinal_position
    """).fetchall()

    for column_name, data_type in rows:
        print(f"{column_name:<35} {data_type}")