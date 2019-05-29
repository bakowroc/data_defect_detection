import time_uuid

from db.models.DataPoint import DataPoint
from db.models.DataSetMap import DataSetMap
from outlier_detector.OutlierDetector import OutlierDetector
from run_all.PlotDrawer import PlotDrawer
from run_all.TestCase import TestCase
from run_all.TestComparator import TestComparator

TEST_DATASETS = [
    [899, 'OYTAL', 'RNC_165'],
    [899, 'OYTAL', 'RNC_5464'],
    [53, 'MOGILA', 'LTE_1079'],
    [53, 'NOGALES', 'MGW_1123'],
    [53, 'NOGALES', 'MGW_2069'],
    [53, 'NOGALES', 'MSC_2250'],
    [53, 'NOGALES', 'MSC_601'],
    [53, 'OCNITA', 'RNC_1883'],
    [53, 'OCNITA', 'RNC_5070'],
    [53, 'OCNITA', 'RNC_615'],
    [534, 'AGUA_PRIETA', 'LTE_1079'],
    [534, 'AGUA_PRIETA', 'LTE_5060'],
    [534, 'AGUA_PRIETA', 'LTE_1079'],
    [534, 'AGUA_PRIETA', 'LTE_5137'],
    [534, 'AGUA_PRIETA', 'LTE_7013'],
    [998, 'DARHAN', 'SGSN_525'],
    [998, 'DARHAN', 'SGSN_544'],
    [998, 'DARHAN', 'SGSN_776'],
    [160, 'MOTUL', 'RNC_19'],
    [160, 'MOTUL', 'RNC_5464'],
    [160, 'MOTUL', 'RNC_1883'],
    [283, 'VILANI', 'RNC_1883'],
    [283, 'VILANI', 'RNC_5081'],
    [283, 'VILANI', 'RNC_5464'],
    [283, 'ORIZABA', 'LTE_5003'],
    [283, 'ORIZABA', 'LTE_5058'],
    [283, 'ORIZABA', 'LTE_5191'],
    [283, 'ORIZABA', 'LTE_5432'],
    [1162, 'SIBU', 'RNC_165'],
    [1162, 'SIBU', 'RNC_1906'],
    [1162, 'SIBU', 'RNC_5082'],
]

TEST_COMPARATORS = [
    TestComparator('feature', [
        TestCase({'feature': 'none'}),
        TestCase({'feature': 'day'}),
        TestCase({'feature': 'weekday'}),
        TestCase({'feature': 'monthday'})
    ]),
    TestComparator('precision', [
        TestCase({'feature': 'day', 'precision': 0.5}),
        TestCase({'feature': 'day', 'precision': 0.75}),
        TestCase({'feature': 'day', 'precision': 1}),
    ]),
    TestComparator('clusters', [
        TestCase({'feature': 'day', 'clusters': 10}),
        TestCase({'feature': 'day', 'clusters': 15}),
        TestCase({'feature': 'day', 'clusters': 20}),
        TestCase({'feature': 'day', 'clusters': 30}),
        TestCase({'feature': 'day', 'clusters': 50}),
        TestCase({'feature': 'day', 'clusters': 80}),
    ], ['sim', 'dist_c', 'dist_f']),
    TestComparator('distance_ratio', [
        TestCase({'feature': 'day', 'distance_ratio': 1}),
        TestCase({'feature': 'day', 'distance_ratio': 2}),
        TestCase({'feature': 'day', 'distance_ratio': 4}),
        TestCase({'feature': 'day', 'distance_ratio': 5}),
        TestCase({'feature': 'day', 'distance_ratio': 7}),
    ], ['dist_c']),
    TestComparator('similarity', [
        TestCase({'feature': 'day', 'similarity': 2}),
        TestCase({'feature': 'day', 'similarity': 3}),
        TestCase({'feature': 'day', 'similarity': 4.5}),
        TestCase({'feature': 'day', 'similarity': 5}),
        TestCase({'feature': 'day', 'similarity': 7}),
    ], ['sim']),
    TestComparator('tolerance', [
        TestCase({'feature': 'day', 'tolerance': 0.25}),
        TestCase({'feature': 'day', 'tolerance': 0.3}),
        TestCase({'feature': 'day', 'tolerance': 0.5}),
        TestCase({'feature': 'day', 'tolerance': 0.8}),
        TestCase({'feature': 'day', 'tolerance': 0.95}),
    ], ['reg']),
]


def run_all(with_calculations=True):
    print("Calculating outliers for all defined algorithms")
    if len(DataSetMap.objects.limit(1)) is 0:
        raise ResourceWarning("collection data_set_map is empty")

    if with_calculations:
        for dataset in TEST_DATASETS:
            print("Calculating dataset {}".format(dataset))

            operator_id = dataset[0]
            acronym = dataset[1]
            kpi_name = dataset[2]

            data_points = DataPoint.objects.filter(operator_id=operator_id, acronym=acronym, kpi_name=kpi_name)
            for comparator in TEST_COMPARATORS:
                comparator.save_dataset(dataset)

                for test in comparator.get_test_cases():
                    configuration = test.get_configuration()
                    detector = OutlierDetector(dataset=parse_result(data_points), feature=configuration['feature'])

                    result_dict = detector.fusion(configuration, algorithms=comparator.get_algorithms())
                    test.append_results(result_dict)

                comparator.generate_csv()

    draw_plots()


def draw_plots():
    for comparator in TEST_COMPARATORS:
        drawer = PlotDrawer('avg', comparator.get_parameter())
        drawer.draw()


def parse_result(data_set):
    parsed_result = []
    for index, data_point in enumerate(data_set):
        parsed_result.append({
            'id': index,
            'value': data_point.value,
            'date': str(time_uuid.TimeUUID.convert(data_point.date).get_datetime()),
            'timestamp': time_uuid.TimeUUID.convert(data_point.date).get_timestamp()
        })

    return parsed_result
