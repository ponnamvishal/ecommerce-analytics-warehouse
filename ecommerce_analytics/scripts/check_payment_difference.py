import duckdb

DB_PATH = r"C:\Users\VISHAL\ecommerce-analytics-warehouse\warehouse.duckdb"

con = duckdb.connect(DB_PATH)

query = """
WITH item_revenue AS (
    SELECT
        order_id,
        SUM(price + freight_value) AS item_revenue
    FROM intermediate.int_order_items_enriched
    GROUP BY order_id
),

payment_totals AS (
    SELECT
        order_id,
        SUM(payment_value) AS payment_value
    FROM staging.stg_order_payments
    GROUP BY order_id
),

comparison AS (
    SELECT
        i.order_id,
        i.item_revenue,
        p.payment_value,
        p.payment_value - i.item_revenue AS difference
    FROM item_revenue i
    JOIN payment_totals p
        ON i.order_id = p.order_id
)

SELECT
    COUNT(*) AS itemized_orders,
    SUM(payment_value) AS total_payment_value,
    SUM(item_revenue) AS total_item_revenue,
    SUM(difference) AS total_difference,

    SUM(
        CASE WHEN difference > 0.01
        THEN difference ELSE 0 END
    ) AS positive_difference,

    SUM(
        CASE WHEN difference < -0.01
        THEN difference ELSE 0 END
    ) AS negative_difference,

    COUNT(
        CASE WHEN difference > 0.01
        THEN 1 END
    ) AS payment_greater_orders,

    COUNT(
        CASE WHEN difference < -0.01
        THEN 1 END
    ) AS revenue_greater_orders,

    COUNT(
        CASE WHEN ABS(difference) <= 0.01
        THEN 1 END
    ) AS approximately_equal_orders

FROM comparison;
"""

result = con.execute(query).fetchone()

columns = [
    "Itemized orders",
    "Total payment value",
    "Total item revenue",
    "Total difference",
    "Positive difference",
    "Negative difference",
    "Payment > revenue orders",
    "Revenue > payment orders",
    "Approximately equal orders",
]

for column, value in zip(columns, result):
    print(f"{column:<35}: {value}")

con.close()