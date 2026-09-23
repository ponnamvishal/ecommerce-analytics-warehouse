import duckdb

DB_PATH = r"C:\Users\VISHAL\ecommerce-analytics-warehouse\warehouse.duckdb"

con = duckdb.connect(DB_PATH)

query = """
WITH item_orders AS (
    SELECT DISTINCT order_id
    FROM intermediate.int_order_items_enriched
),

payment_orders AS (
    SELECT DISTINCT order_id
    FROM staging.stg_order_payments
)

SELECT
    p.order_id,
    SUM(p.payment_value) AS payment_value
FROM staging.stg_order_payments p
WHERE p.order_id IN (
    SELECT order_id
    FROM payment_orders
    EXCEPT
    SELECT order_id
    FROM item_orders
)
GROUP BY p.order_id
ORDER BY payment_value DESC;
"""

rows = con.execute(query).fetchall()

print("Payment orders without item records:", len(rows))

for order_id, payment_value in rows:
    print(f"{order_id} : {payment_value}")

con.close()