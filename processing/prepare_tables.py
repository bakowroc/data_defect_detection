from db.models.OperatorToAcronym import OperatorToAcronym

def prepare_info_tables(db, value_data_list):
    operator_acronym_map = create_operator_acronym_map(value_data_list)
    fill_operator_to_acronym(db, operator_acronym_map)


def create_operator_acronym_map(value_data_list):
    return set(map(lambda value_data: (value_data.operator_id, value_data.acronym), value_data_list))


def fill_operator_to_acronym(db, map):
    print("-> Filling table operator_to_acronym")
    for operator_acronym_pair in map:
        operator_id = operator_acronym_pair[0]
        acronym = operator_acronym_pair[1]
        db.execute_query(OperatorToAcronym(operator_id, acronym).insert())