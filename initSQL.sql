CREATE TABLE kpi_defs(
    parition_key text,
    definition_id double PRIMARY KEY,,
    calculator_class text,
    weight double,
    formula text,
    isA boolean,
    isB boolean,
    isC boolean,
    A text,
    B text,
    C text,
    D text,
    calc text,
    E text,
    date timestamp,
    F text,
    G text,
    H text,
    second_date timestamp,
    nr_A double,
    tags text,
    technology text,
    description text,
    thresholds text,
    unit text,
    isDel boolean
);

COPY kpi_defs(parition_key, definition_id, calculator_class, weight, formula, isA, isB, isC, a, b, c, d, calc, e, date, f, g, h, second_date, nr_a, tags, technology, description, thresholds, unit, isdel) FROM 'defs.csv';

CREATE TABLE raw_data(
  kpi_name TEXT,
  kpi_basename TEXT,
  kpi_version TEXT,
  cord_id BIGINT,
  acronym TEXT,
  date TIMESTAMP,
  value DOUBLE,
  to_be_deleted BOOLEAN,
  PRIMARY KEY(kpi_basename, date)
);

COPY raw_data(kpi_basename, date, cord_id, acronym, kpi_name, kpi_version, to_be_deleted, value) FROM 'plmn.csv';