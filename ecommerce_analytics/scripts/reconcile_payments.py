import duckdb

DB_PATH = r"C:\Users\VISHAL\ecommerce-analytics-warehouse\warehouse.duckdb"

with duckdb.connect(DB_PATH) as con:

    query = """
        WITH itemized_orders AS (
            SELECT DISTINCT order_id
            FROM raw.order_items
        ),

        payment_summary AS (
            SELECT
                p.order_id,
                SUM(p.payment_value) AS payment_value
            FROM raw.order_payments p
            GROUP BY p.order_id
        )

        SELECT
            COUNT(*) AS orders_without_items,
            ROUND(SUM(ps.payment_value), 2) AS payment_value_without_items
        FROM payment_summary ps
        LEFT JOIN itemized_orders io
            ON ps.order_id = io.order_id
        WHERE io.order_id IS NULL
    """

    result = con.execute(query).fetchone()

    print(f"Orders without items   : {result[0]}")
    print(f"Payment value          : {result[1]}")