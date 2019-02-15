from bisect import bisect_right
import datetime

def count_text_bytes(sentence):
    cumulative_sum = [0]
    for c in sentence:
        if 0 <= ord(c) <= 4351 or 8192 <= ord(c) <= 8205 or 8208 <= ord(c) <= 8223 or 8242 <= ord(c) <= 8247:
            cumulative_sum.append(cumulative_sum[-1] + 1)
        else:
            cumulative_sum.append(cumulative_sum[-1] + 2)
    return cumulative_sum[1:]

def trim(sentence):
    return sentence[:bisect_right(count_text_bytes(sentence), 280)]
