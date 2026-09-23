SELECT
    order_id,
    order_item_id,
    COUNT(*) AS row_count
FROM {{ ref('int_order_items_enriched') }}
GROUP BY
    order_id,
    order_item_id
HAVING COUNT(*) > 1