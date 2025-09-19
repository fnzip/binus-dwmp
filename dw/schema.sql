CREATE TABLE dim_sex (
    sex_id SERIAL PRIMARY KEY,
    sex VARCHAR(10) UNIQUE
);

CREATE TABLE dim_smoker (
    smoker_id SERIAL PRIMARY KEY,
    status VARCHAR(10) UNIQUE
);

CREATE TABLE dim_region (
    region_id SERIAL PRIMARY KEY,
    region VARCHAR(20) UNIQUE
);

CREATE TABLE dim_age (
    age_id SERIAL PRIMARY KEY,
    age_group VARCHAR(20) UNIQUE
);

CREATE TABLE dim_children (
    children_id SERIAL PRIMARY KEY,
    jumlah_anak INT UNIQUE
);

CREATE TABLE fact_insurance (
    insurance_id SERIAL PRIMARY KEY,
    age_id INT REFERENCES dim_age(age_id),
    sex_id INT REFERENCES dim_sex(sex_id),
    bmi FLOAT,
    children_id INT REFERENCES dim_children(children_id),
    smoker_id INT REFERENCES dim_smoker(smoker_id),
    region_id INT REFERENCES dim_region(region_id),
    charges FLOAT
);
