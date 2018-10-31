def filter_complex_kpis(kpis):
    result = []

    for kpi in kpis:
        if kpi.formula.count('[') == 1:
            result.append(kpi)

    return result


def filter_not_matched_data(raw_data, kpi_names):
    if raw_data.kpi_name in kpi_names:
        return raw_data


