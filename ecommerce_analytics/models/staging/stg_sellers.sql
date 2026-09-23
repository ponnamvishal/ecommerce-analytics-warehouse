SELECT
    seller_id,
    CAST(seller_zip_code_prefix AS INTEGER) AS seller_zip_code_prefix,
    TRIM(LOWER(seller_city)) AS seller_city,
    UPPER(TRIM(seller_state)) AS seller_state
FROM {{ source('raw', 'sellers') }}