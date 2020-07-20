CREATE SCHEMA IF NOT EXISTS covid;

CREATE TABLE IF NOT EXISTS covid.countries_aggregated (
    date timestamp,
    country TEXT,
    confirmed integer,
    recovered integer,
    deaths integer,
    PRIMARY KEY (date, country)
);

CREATE TABLE IF NOT EXISTS covid.countries_ref (
    uid integer,
    iso2 TEXT,
    iso3 TEXT,
    code3 integer,
    fips integer,
    admin2 TEXT,
    province_state TEXT,
    country_region TEXT,
    lat float(2),
    long_ float(2),
    combined_key TEXT,
    population integer,
    PRIMARY KEY (uid)
);

CREATE TABLE IF NOT EXISTS covid.us_aggregated (
    uid integer,
    date timestamp,
    confirmed integer,
    deaths integer,
    PRIMARY KEY (uid, date)
);
