CREATE TABLE task (
    task_id BIGSERIAL PRIMARY KEY,
    start_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    manager_params TEXT,
    openwpm_version TEXT,
    browser_version TEXT
);

CREATE TABLE crawl (
    browser_id BIGSERIAL PRIMARY KEY,
    task_id BIGSERIAL,
    browser_params TEXT,
    start_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dns_responses (
    id BIGSERIAL PRIMARY KEY,
    request_id BIGSERIAL,
    browser_id BIGSERIAL,
    visit_id BIGINT,
    hostname TEXT,
    addresses TEXT,
    used_address TEXT,
    canonical_name TEXT,
    time_stamp TIMESTAMPTZ
);

CREATE TABLE javascript_cookies (
    id BIGSERIAL PRIMARY KEY,
    browser_id BIGSERIAL,
    visit_id BIGSERIAL,
    extension_session_uuid TEXT,
    event_ordinal SERIAL,
    record_type TEXT,
    change_cause TEXT,
    expiry TIMESTAMPTZ,
    is_http_only SMALLINT,
    is_host_only SMALLINT,
    is_session SMALLINT,
    host TEXT,
    is_secure SMALLINT,
    name TEXT,
    path TEXT,
    value TEXT,
    same_site TEXT,
    first_party_domain TEXT,
    store_id TEXT,
    time_stamp TIMESTAMPTZ
);

CREATE TABLE site_visits (
    visit_id BIGSERIAL PRIMARY KEY,
    browser_id BIGSERIAL,
    site_url TEXT,
    site_rank BIGINT
);

ALTER TABLE crawl
    ADD constraint FK_task_id_task
    FOREIGN KEY (task_id)
    REFERENCES task(task_id);

ALTER TABLE site_visits
    ADD constraint FK_browser_id_crawl
    FOREIGN KEY (browser_id)
    REFERENCES crawl(browser_id);