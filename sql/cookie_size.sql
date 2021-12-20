CREATE TABLE cookie_size AS
    SELECT DISTINCT host, name, octet_length(CONCAT(name, '=', value, ';path=', path)) AS byte_size
    FROM javascript_cookies;