WITH customer_orders AS (

    SELECT
        customer_unique_id,
        order_id,
        order_status,
        order_purchase_timestamp,
        price,
        freight_value,
        item_total_including_freight
    FROM {{ ref('int_order_items_enriched') }}

),

customer_summary AS (

    SELECT
        customer_unique_id,

        COUNT(DISTINCT order_id) AS total_orders,

        COUNT(DISTINCT CASE
            WHEN order_status = 'delivered' THEN order_id
        END) AS delivered_orders,

        COUNT(*) AS total_items,

        SUM(price) AS total_product_revenue,

        SUM(freight_value) AS total_freight,

        SUM(item_total_including_freight) AS total_revenue,

        MIN(order_purchase_timestamp) AS first_order_date,

        MAX(order_purchase_timestamp) AS last_order_date

    FROM customer_orders

    GROUP BY
        customer_unique_id

)

SELECT
    customer_unique_id,
    total_orders,
    delivered_orders,
    total_items,
    total_product_revenue,
    total_freight,
    total_revenue,

    ROUND(
        total_revenue / NULLIF(total_orders, 0),
        2
    ) AS average_order_value,

    first_order_date,
    last_order_date,

    DATE_DIFF(
        'day',
        CAST(first_order_date AS DATE),
        CAST(last_order_date AS DATE)
    ) AS customer_lifetime_days

FROM customer_summary