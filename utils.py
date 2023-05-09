import math

from difflib import SequenceMatcher

# from dump import dump


def replace_most_similar_chunk(whole, part, replace):
    similarity_thresh = 0.8
    max_similarity = 0
    most_similar_chunk_start = -1
    most_similar_chunk_end = -1

    whole_lines = whole.splitlines()
    part_lines = part.splitlines()

    scale = 0.1
    min_len = math.floor(len(part_lines) * (1 - scale))
    max_len = math.ceil(len(part_lines) * (1 + scale))

    for length in range(min_len, max_len):
        for i in range(len(whole_lines) - length + 1):
            chunk = whole_lines[i : i + length + 1]
            chunk = "\n".join(chunk)

            similarity = SequenceMatcher(None, chunk, part).ratio()

            if similarity > max_similarity and similarity:
                max_similarity = similarity
                most_similar_chunk_start = i
                most_similar_chunk_end = i + length + 1

    if max_similarity < similarity_thresh:
        return

    replace_lines = replace.splitlines()
    modified_whole = (
        whole_lines[:most_similar_chunk_start]
        + replace_lines
        + whole_lines[most_similar_chunk_end:]
    )
    modified_whole = "\n".join(modified_whole)
    return modified_whole