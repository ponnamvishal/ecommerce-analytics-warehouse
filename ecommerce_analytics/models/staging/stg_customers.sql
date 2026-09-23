SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    TRIM(LOWER(customer_city)) AS customer_city,
    UPPER(TRIM(customer_state)) AS customer_state
FROM {{ source('raw', 'customers') }}