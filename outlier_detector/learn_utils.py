import numpy as np


def create_windows(data, window_len, slide_len):
    chunks = []
    for pos in range(0, len(data), slide_len):
        chunk = np.copy(data[pos:pos + window_len])
        chunks.append(chunk)

    return chunks
