WITH product_metrics AS (

    SELECT
        product_id,

        -- Product information
        MAX(category_name) AS category_name,
        MAX(product_category_name_english) AS category_name_english,

        -- Sales metrics
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(*) AS total_items_sold,

        -- Revenue metrics
        SUM(price) AS product_revenue,
        SUM(freight_value) AS total_freight,
        SUM(item_total_including_freight) AS total_revenue,

        -- Pricing metrics
        AVG(price) AS average_item_price,
        AVG(freight_value) AS average_freight_value,

        -- Product information
        MAX(product_name_length) AS product_name_length,
        MAX(product_description_length) AS product_description_length,
        MAX(product_photos_qty) AS product_photos_qty,

        -- Physical attributes
        MAX(product_weight_g) AS product_weight_g,
        MAX(product_length_cm) AS product_length_cm,
        MAX(product_height_cm) AS product_height_cm,
        MAX(product_width_cm) AS product_width_cm

    FROM {{ ref('int_order_items_enriched') }}

    GROUP BY product_id

)

SELECT
    product_id,
    category_name,
    category_name_english,

    total_orders,
    total_items_sold,

    product_revenue,
    total_freight,
    total_revenue,

    average_item_price,
    average_freight_value,

    product_name_length,
    product_description_length,
    product_photos_qty,

    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm

FROM product_metrics