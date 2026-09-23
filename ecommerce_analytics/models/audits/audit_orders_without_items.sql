WITH orders_without_items AS (

    SELECT
        o.order_id,
        o.order_status
    FROM {{ ref('stg_orders') }} AS o

    LEFT JOIN {{ ref('stg_order_items') }} AS oi
        ON o.order_id = oi.order_id

    WHERE oi.order_id IS NULL
),

unexpected_orders AS (

    SELECT *
    FROM orders_without_items

    WHERE order_status NOT IN (
        'unavailable',
        'canceled',
        'created'
    )
)

SELECT *
FROM unexpected_orders