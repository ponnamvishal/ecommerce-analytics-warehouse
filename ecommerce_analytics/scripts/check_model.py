import duckdb

DB_PATH = r"C:\Users\VISHAL\ecommerce-analytics-warehouse\warehouse.duckdb"

with duckdb.connect(DB_PATH) as con:

    rows = con.execute("""
        SELECT
            table_schema,
            table_name
        FROM information_schema.tables
        WHERE table_name = 'int_order_items_enriched'
    """).fetchall()

    for row in rows:
        print(f"schema={row[0]}, table={row[1]}")