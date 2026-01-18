-- Example query
SELECT
    id AS user_id,
    name AS user_name
FROM
    users
WHERE
    active = TRUE
