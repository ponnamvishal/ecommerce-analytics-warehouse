WITH daily_sales AS (

    SELECT
        CAST(order_purchase_timestamp AS DATE) AS sales_date,

        COUNT(DISTINCT order_id) AS total_orders,

        COUNT(*) AS total_items,

        SUM(price) AS product_revenue,

        SUM(freight_value) AS total_freight,

        SUM(item_total_including_freight) AS total_revenue

    FROM {{ ref('int_order_items_enriched') }}

    GROUP BY
        CAST(order_purchase_timestamp AS DATE)

)

SELECT
    sales_date,
    total_orders,
    total_items,
    product_revenue,
    total_freight,
    total_revenue,

    CASE
        WHEN total_orders > 0
        THEN total_revenue / total_orders
        ELSE 0
    END AS average_order_value

FROM daily_sales