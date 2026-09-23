WITH order_items AS (

    SELECT
        order_id,
        order_item_id,
        product_id,
        seller_id,
        shipping_limit_date,
        price,
        freight_value
    FROM {{ ref('stg_order_items') }}

),

orders AS (

    SELECT
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp,
        order_approved_at,
        order_delivered_carrier_date,
        order_delivered_customer_date,
        order_estimated_delivery_date
    FROM {{ ref('stg_orders') }}

),

customers AS (

    SELECT
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    FROM {{ ref('stg_customers') }}

),

products AS (

    SELECT
        product_id,
        product_category_name,
        product_name_length,
        product_description_length,
        product_photos_qty,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm
    FROM {{ ref('stg_products') }}

),

sellers AS (

    SELECT
        seller_id,
        seller_zip_code_prefix,
        seller_city,
        seller_state
    FROM {{ ref('stg_sellers') }}

),

category_translation AS (

    SELECT
        product_category_name,
        product_category_name_english
    FROM {{ ref('stg_category_translation') }}

)

SELECT

    -- Order item grain
    oi.order_id,
    oi.order_item_id,

    -- Customer
    o.customer_id,
    c.customer_unique_id,
    c.customer_zip_code_prefix,
    c.customer_city,
    c.customer_state,

    -- Order
    o.order_status,
    CAST(o.order_purchase_timestamp AS TIMESTAMP) AS order_purchase_timestamp,
    CAST(o.order_approved_at AS TIMESTAMP) AS order_approved_at,
    CAST(o.order_delivered_carrier_date AS TIMESTAMP) AS order_delivered_carrier_date,
    CAST(o.order_delivered_customer_date AS TIMESTAMP) AS order_delivered_customer_date,
    CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS order_estimated_delivery_date,

    -- Product
    oi.product_id,
    p.product_category_name,
    ct.product_category_name_english,

    COALESCE(
        ct.product_category_name_english,
        p.product_category_name,
        'unknown'
    ) AS category_name,

    p.product_name_length,
    p.product_description_length,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm,

    -- Seller
    oi.seller_id,
    s.seller_zip_code_prefix,
    s.seller_city,
    s.seller_state,

    -- Financial measures
    oi.price,
    oi.freight_value,

    oi.price + oi.freight_value AS item_total_including_freight

FROM order_items oi

LEFT JOIN orders o
    ON oi.order_id = o.order_id

LEFT JOIN customers c
    ON o.customer_id = c.customer_id

LEFT JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN sellers s
    ON oi.seller_id = s.seller_id

LEFT JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name