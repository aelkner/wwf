import os
import sys
import pickle


def run(cmd):
    print(cmd)
    os.system(cmd)


def popen(cmd):
    print(cmd)
    return os.popen(cmd)


def get_mem_size(words):
    return sys.getsizeof(words)


def save_words(words):
    filename = os.path.dirname(__file__) + '/words.p'
    pickle.dump(words, open(filename, 'wb'))


def load_words():
    filename = os.path.dirname(__file__) + '/words.p'
    words = pickle.load(open(filename, 'rb'))
    return [
        word for word in words if word not in [
            'rez',
            'uni',
        ]
    ] + [
        'di',
    ]


def save_wwf_words():
    def get_wwf_words_for_letter(letter):
        words = []
        for index in range(2, 16):
            cmd = 'curl http://scrabble.merriam.com/lapi/1/sbl_finder/get_limi'
            cmd += 'ted_data -d "mode=wfd&type=begins&rack={letter}&len={len}"'
            cmd = cmd.format(letter=letter, len=index)
            payload = popen(cmd).read()
            dct = eval(payload)
            words.extend(dct['data'])
        return words

    words = []
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        words.extend(get_wwf_words_for_letter(letter))
    save_words(words)


def filter_words(words, opts, filters):
    for opt, filter in zip(opts, filters):
        filter_list = filter.split('/')
        apply_filter = {
            's': lambda word: [
                0 for filter in filter_list if word.startswith(filter)
            ],
            'e': lambda word: [
                0 for filter in filter_list if word.endswith(filter)
            ],
            'c': lambda word: [
                0 for filter in filter_list if filter in word
            ],
        }[opt]
        words = [
            word for word in words if apply_filter(word)
        ]
    return words


def build_buckets(words):
    buckets = []
    for word in words:
        word_index = len(word) - 2
        if word_index > len(buckets) - 1:
            for _ in range(word_index - len(buckets) + 1):
                buckets.append([])
        buckets[word_index].append(word)
    return buckets


def print_buckets(buckets):
    results = []
    for index, bucket in enumerate(buckets):
        results.append('    {size}: {words}'.format(
            size=index+2, words=' '.join(bucket)
        ))
    for result in reversed(results):
        print(result)
