def filter_complex_kpis(kpis):
    result = []

    for kpi in kpis:
        if kpi.formula is not None and kpi.formula.count('[') == 1:
            result.append(kpi)

    return result


def filter_not_matched_data(raw_data, kpi_names):
    result = []

    if raw_data.kpi_name in kpi_names:
        result.append(raw_data)

    return result

