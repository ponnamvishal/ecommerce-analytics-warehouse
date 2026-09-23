import duckdb

DB_PATH = r"C:\Users\VISHAL\ecommerce-analytics-warehouse\warehouse.duckdb"

with duckdb.connect(DB_PATH) as con:

    checks = {
        "customer_count": """
            SELECT COUNT(*)
            FROM marts.mart_customer_summary
        """,

        "duplicate_customers": """
            SELECT COUNT(*)
            FROM (
                SELECT customer_unique_id
                FROM marts.mart_customer_summary
                GROUP BY customer_unique_id
                HAVING COUNT(*) > 1
            )
        """,

        "null_customer_ids": """
            SELECT COUNT(*)
            FROM marts.mart_customer_summary
            WHERE customer_unique_id IS NULL
        """,

        "null_total_revenue": """
            SELECT COUNT(*)
            FROM marts.mart_customer_summary
            WHERE total_revenue IS NULL
        """,

        "total_revenue": """
            SELECT ROUND(SUM(total_revenue), 2)
            FROM marts.mart_customer_summary
        """,

        "total_orders": """
            SELECT SUM(total_orders)
            FROM marts.mart_customer_summary
        """
    }

    for name, query in checks.items():
        result = con.execute(query).fetchone()[0]
        print(f"{name:<25} {result}")
        