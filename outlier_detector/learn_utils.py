import numpy as np
import collections


def create_windows(data, window_len, slide_len):
    chunks = []
    for pos in range(0, len(data), slide_len):
        chunk = np.copy(data[pos:pos + window_len])
        chunks.append(chunk)

    return chunks


def to_clusters(dataset, labels):
    current_label = labels[0]
    current_cluster = []
    clusters = []
    clusters_dict = {}

    for index, label in enumerate(labels):
        if label != current_label:
            clusters.append(current_cluster)
            clusters_dict[current_label] = current_cluster
            current_cluster = [dataset[index]]
        else:
            current_cluster.append(dataset[index])

        current_label = label

    clusters_dict[current_label] = current_cluster

    return clusters[:1], clusters_dict


def create_points_with_labels(dataset, labels):
    dataset_with_labels = []
    for index, data_point in enumerate(dataset):
        point_with_label = data_point
        point_with_label['label'] = int(labels[index])
        dataset_with_labels.append(point_with_label)

    return dataset_with_labels


def flatten(to_flat_list):
    flat_list = []
    for x in to_flat_list:
        for item in x:
            flat_list.append(item)

    return flat_list


def count_duplicates(arg):
    return collections.Counter(arg)
