SELECT
    CAST(geolocation_zip_code_prefix AS INTEGER) AS zip_code_prefix,
    CAST(geolocation_lat AS DOUBLE) AS latitude,
    CAST(geolocation_lng AS DOUBLE) AS longitude,
    TRIM(LOWER(geolocation_city)) AS city,
    UPPER(TRIM(geolocation_state)) AS state

FROM {{ source('raw', 'geolocation') }}