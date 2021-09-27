CREATE TABLE dns_responses (
    id SERIAL PRIMARY KEY,
    request_id BIGINT,
    browser_id BIGINT,
    visit_id BIGINT,
    hostname TEXT,
    addresses TEXT,
    used_address TEXT,
    canonical_name TEXT,
    time_stamp TIMESTAMPTZ
);

CREATE TABLE javascript_cookies (
    id SERIAL PRIMARY KEY,
    browser_id BIGINT,
    visit_id BIGINT,
    extension_session_uuid TEXT,
    event_ordinal SERIAL,
    record_type TEXT,
    change_cause TEXT,
    expiry TIMESTAMPTZ,
    is_http_only BOOLEAN,
    is_host_only BOOLEAN,
    is_session BOOLEAN,
    host TEXT,
    is_secure BOOLEAN,
    name TEXT,
    path TEXT,
    value TEXT,
    same_site TEXT,
    first_party_domain TEXT,
    store_id TEXT,
    time_stamp TIMESTAMPTZ
);

CREATE TABLE site_visits (
    visit_id BIGINT PRIMARY KEY,
    browser_id BIGINT,
    site_url TEXT,
    site_rank BIGINT
);