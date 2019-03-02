CREATE TABLE data_det.raw_kpi_definitions (
    partition_key text,
    id int,
    calculator_class text,
    decimal_places int,
    formula text,
    highest_is_best boolean,
    is_active boolean,
    is_simple boolean,
    max double,
    min double,
    nekpi_aggr_by_period_cl_at timestamp,
    nekpi_calc_at timestamp,
    period_calculator_class text,
    plmnkpi_aggr_by_cord_at timestamp,
    plmnkpi_aggr_by_cord_group_at timestamp,
    plmnkpi_aggr_by_period_at timestamp,
    plmnkpi_aggr_by_period_cl_at timestamp,
    plmnkpi_aggr_by_region_at timestamp,
    plmnkpi_calc_at timestamp,
    priority int,
    tags text,
    technology text,
    text text,
    thresholds list<double>,
    unit text,
    use_thresholds boolean,
    PRIMARY KEY (partition_key, id)
);

CREATE TABLE data_det.kpi_definitions (
    id int,
    formula text,
    tags text,
    technology text,
    description text,
    unit text,
    PRIMARY KEY (id)
);

CREATE TABLE data_det.raw_data_points (
    kpi_basename text,
    date timestamp,
    cord_id bigint,
    acronym text,
    kpi_name text,
    kpi_version text,
    to_be_deleted boolean,
    value double,
    PRIMARY KEY (kpi_basename, date, cord_id, acronym)
);

CREATE TABLE data_det.data_points (
    operator_id bigint,
    acronym text,
    kpi_name text,
    date timeuuid,
    value double,
    PRIMARY KEY (operator_id, acronym, kpi_name, date)
);

CREATE TABLE data_det.data_set_map (
    operator_id bigint,
    acronym text,
    kpi_name text,
    PRIMARY KEY (operator_id, acronym, kpi_name)
);

CREATE TABLE data_det.acronym_name_map (
    raw_acronym text,
    acronym text,
    PRIMARY KEY (raw_acronym, acronym)
);
