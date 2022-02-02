CREATE TABLE site_total AS
    SELECT visit_id, REGEXP_REPLACE(site_url, '^\s*(www\.|https?:\/\/www\.|http?:\/\/www\.|http?:\/\/|https?:\/\/)', '') AS site_url
    FROM site_visits

CREATE TABLE sites AS WITH
    javascript_cookies_table AS (
        SELECT visit_id, site_url, name, time_stamp
        FROM site_total
            NATURAL LEFT JOIN javascript_cookies
        WHERE record_type = 'added-or-changed'
    ),
    cookies_per_visit AS (
        /*
        visit_id,
        site_url,
        n_cookies: the number of cookies per visit_id
        */
        SELECT site_total.visit_id, site_total.site_url, COUNT(javascript_cookies_table.name) AS n_cookies
        FROM site_total
            LEFT JOIN javascript_cookies_table ON site_total.visit_id = javascript_cookies_table.visit_id
        GROUP BY site_total.visit_id, site_total.site_url
        ),
    visits_with_max_cookies AS (
        /* For every site_url: get the visit_id with the most cookies
        Note: Two visit_ids could have the same (max) amount of cookies
        */
        SELECT visit_id, site_url, n_cookies
        FROM (
            SELECT visit_id, site_url, n_cookies,
                MAX(n_cookies) OVER (PARTITION BY site_url) AS max_n_cookies
            FROM cookies_per_visit
            ) temp
        WHERE max_n_cookies = n_cookies
    ),
    max_visit_id_max_cookies AS (
        /* Get the highest `visit_id` per site_url, one visit_id per site_url */
        SELECT visit_id, site_url, n_cookies
        FROM (
            SELECT visit_id,
                site_url,
                n_cookies,
                MAX(visit_id) OVER (PARTITION BY site_url) AS max_visit_id
            FROM visits_with_max_cookies
        ) temp
        WHERE visit_id = max_visit_id
    )
    SELECT visit_id, max.site_url, n_cookies, ranking
    FROM max_visit_id_max_cookies max LEFT JOIN site_ranking sr ON max.site_url = sr.site_url
    ORDER BY ranking;

CREATE TABLE cookies AS
    SELECT jc.*
    FROM sites LEFT JOIN javascript_cookies jc on sites.visit_id = jc.visit_id
    WHERE record_type = 'added-or-changed';

CREATE TABLE dns AS
    SELECT dr.*
    FROM sites LEFT JOIN dns_responses dr ON sites.visit_id = dr.visit_id;

CREATE TABLE cookies_size AS
    SELECT DISTINCT host, name, octet_length(CONCAT(name, value)) AS byte_size
    FROM cookies;