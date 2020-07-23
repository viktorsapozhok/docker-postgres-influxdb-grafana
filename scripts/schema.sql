CREATE SCHEMA IF NOT EXISTS covid;

CREATE TABLE covid.countries_ref(
    uid INTEGER NOT NULL PRIMARY key,
    iso2 VARCHAR(2),
    iso3 VARCHAR(3),
    code3 INTEGER,
    fips INTEGER,
    admin2 VARCHAR(41),
    province_state VARCHAR(40),
    country_region VARCHAR(32),
    lat NUMERIC(11,8),
    long_ NUMERIC(13,9),
    combined_key VARCHAR(55),
    population INTEGER
);

CREATE TABLE covid.countries_aggregated(
   date DATE NOT NULL,
   country VARCHAR(32) NOT NULL,
   confirmed INTEGER,
   recovered INTEGER,
   deaths INTEGER,
   PRIMARY KEY(date, country)
);

CREATE TABLE covid.us_confirmed(
   uid INTEGER NOT NULL,
   iso2 VARCHAR(2),
   iso3 VARCHAR(3),
   code3 INTEGER,
   fips NUMERIC(7,1),
   admin2 VARCHAR(41),
   lat NUMERIC(19,15),
   combined_key VARCHAR(55),
   date DATE NOT NULL,
   confirmed INTEGER,
   long_ NUMERIC(18,14),
   country_region VARCHAR(32),
   province_state VARCHAR(40),
   PRIMARY KEY (uid, date)
);