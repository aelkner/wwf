import os
import sys
import pickle
import re


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
            'acai', 'afros', 'agro', 'ahis', 'airvac', 'aji', 'alvar', 'apo', 'apos', 'areg', 'atigi', 'automat,'
            'barfi', 'berber', 'bibe', 'bish',
            'cert', 'chuse', 'cleg', 'crit', 'cru', 'cinq', 'crudo',
            'dan', 'das', 'deshi', 'desi', 'dobe', 'doh', 'dohs', 'doobs', 'dum',
            'eco', 'ecos', 'eds', 'eew', 'emerg', 'emo', 'ensuite', 'est', 'exed',
            'factum', 'fah', 'fes',
            'gomer', 'gos',
            'hims', 'hiya',
            'jook', 'juvies',
            'kapu', 'kis',
            'lah', 'lahs', 'larn', 'loto' 'lotter', 'luxer',
            'merc', 'merch', 'moi', 'mux',
            'naes', 'nala', 'nalas', 'nano', 'nanos', 'nav', 'navs', 'nazi', 'nazis', 'neg', 'niner', 'niners', 'novate',
                'novated', 'novates', 'nug',
            'oik', 'oiks', 'oof', 'oma', 'opa', 'org', 'owt'
            'pa', 'perc', 'pisher', 'po', 'pos', 'posier',
            'reno', 'rez', 'rosti',
            'samier', 'san', 'sev', 'sevs', 'sig', 'smush', 'soba', 'soc', 'stoved',
            'tec', 'techs', 'tegu', 'thali', 'tiz', 'tolt', 'tum', 'tums', 'turr', 'turrs',
            'uni',
            'vega', 'vetter', 'vin', 'vins', 'vuln',
            'weta',
            'zeda', 'zendo', 'zendos',
        ]
    ] + [
        'di', 'dux',
        'turd',
        'von',
        'zen',
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


def filter_words(words, opts, filters, form):
    for opt, filter_spec in zip(opts, filters):
        filter_parts = filter_spec.split('/')
        if opt == 's':
            apply_filter = lambda word: [
                0 for part in filter_parts if word.startswith(part)
            ]
        elif opt == 'e':
            apply_filter = lambda word: [
                0 for part in filter_parts if word.endswith(part)
            ]
        else:
            macro = form.get('macro', '')
            if filter_spec.startswith('`'):
                filter_parts = filter_spec.split('`')[1:]
            elif macro:
                fs = '['+ filter_spec + ']'
                filter_parts = [
                    macro.replace('$', fs).replace(';', fs + '*').replace(
                        "'", fs + '+')
                ]
            print(filter_parts)
            if filter_spec.startswith('`') or macro:
                apply_filter = lambda word: [
                    0 for part in filter_parts if re.match(part + '$', word)
                ]
            else:
                apply_filter = lambda word: [
                    0 for part in filter_parts if part in word
                ]
        words = list(filter(apply_filter, words))
    return words


def build_buckets(words):
    buckets = []
    for word in words:
        word_index = len(word) - 2
        if word_index > len(buckets) - 1:
            for _ in range(word_index - len(buckets) + 1):
                buckets.append([])
        buckets[word_index].append(word)
    return [
        list(sorted(bucket)) for bucket in buckets
    ]


def print_buckets(buckets):
    results = []
    for index, bucket in enumerate(buckets):
        results.append('    {size}: {words}'.format(
            size=index+2, words=' '.join(bucket)
        ))
    for result in reversed(results):
        print(result)
