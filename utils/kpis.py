import re
from typing import List


def get_names(kpis) -> List[str]:
    kpi_names = []

    for kpi in kpis:
        kpi_name = re.search('\[(.*)\]', kpi.formula)
        kpi_names.append(kpi_name.group(1))

    return kpi_names


def filter_complex_kpis(kpis):
    result = []

    for kpi in kpis:
        if kpi.formula.count('[') == 1:
            result.append(kpi)

    return result


def filter_not_matched_data(raw_data, kpi_names):
    filtered_row = raw_data if raw_data.kpi_name in kpi_names else None
    return filtered_row
