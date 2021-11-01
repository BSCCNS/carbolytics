CREATE TABLE site_visits (
    visit_id SERIAL PRIMARY KEY NOT NULL,
    site_url TEXT
);

CREATE TABLE dns_responses (
    visit_id SERIAL REFERENCES site_visits (visit_id),
    hostname TEXT,
    addresses TEXT,
    used_address TEXT,
    canonical_name TEXT,
    time_stamp TIMESTAMPTZ
);

CREATE TABLE javascript_cookies (
    visit_id SERIAL REFERENCES site_visits (visit_id),
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
    time_stamp TIMESTAMPTZ
);