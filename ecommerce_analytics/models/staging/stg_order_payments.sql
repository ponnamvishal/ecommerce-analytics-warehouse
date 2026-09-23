SELECT
    order_id,
    payment_sequential,
    LOWER(TRIM(payment_type)) AS payment_type,
    CAST(payment_installments AS INTEGER) AS payment_installments,
    CAST(payment_value AS DECIMAL(12, 2)) AS payment_value
FROM {{ source('raw', 'order_payments') }}