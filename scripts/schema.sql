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
    country TEXT,
    lat float(2),
    lon float(2),
    combined_key TEXT,
    population integer,
    PRIMARY KEY (uid)
);
