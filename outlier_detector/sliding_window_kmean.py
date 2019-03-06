from sklearn.cluster import KMeans
import numpy as np

from outlier_detector import learn_utils


def sliding_window_kmean(dataset, n_clusters, segment_len=12, slide=2):
    data = dataset
    window_rads = np.linspace(0, np.pi, segment_len)
    window = np.sin(window_rads)**2
    windowed_segments = get_windowed_segments(data[:(int(len(data) / 2))], window, slide)
    clusterer = KMeans(n_clusters=n_clusters)
    clusterer.fit(windowed_segments)
    reconstruction = learn_utils.reconstruct(data, window, clusterer)
    return reconstruction


def get_windowed_segments(data, window, slide):
    """
    Populate a list of all segments seen in the input data.  Apply a window to
    each segment so that they can be added together even if slightly
    overlapping, enabling later reconstruction.
    """
    windowed_segments = []
    segments = learn_utils.sliding_chunker(
        data,
        window_len=len(window),
        slide_len=slide
    )
    for segment in segments:
        segment *= window
        windowed_segments.append(segment)
    return windowed_segments
