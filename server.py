#!/usr/bin/env python
import os

from bottle import run, route, request, template, static_file

import utils


words = utils.load_words()


@route('/static/<filepath:path>')
def server_static(filepath):
    static_path = os.path.dirname(__file__) + '/static/'
    return static_file(filepath, root=static_path)


@route('/', method='GET')
def get():
    return process_request()


@route('/', method='POST')
def post():
    return process_request()


def process_request():
    starts_with, ends_with, contains = '', '', ''
    if request.forms:
        starts_with = request.forms.get('starts_with', '')
        ends_with = request.forms.get('ends_with', '')
        contains = request.forms.get('contains', '')

    chosen_opts = [
        ('s', starts_with),
        ('e', ends_with),
        ('c', contains),
    ]
    opts, filters = '', []
    for chosen_opt, filter in chosen_opts:
        if filter:
            opts += chosen_opt
            filters.append(filter)
    if not filters:
        filtered_words = []
    else:
        filtered_words = utils.filter_words(words, opts, filters)
    buckets = utils.build_buckets(filtered_words)

    if buckets:
        index, total = 0, 0
        while True:
            total += len(buckets[index])
            if total > 10000:
                break
            index += 1
            if index >= len(buckets):
                break
        buckets = buckets[:index]

    if starts_with:
        focus = 'starts_with'
    elif ends_with:
        focus = 'ends_with'
    elif contains:
        focus = 'contains'
    else:
        focus = 'starts_with'

    template_buckets = [
        {
            'heading': '{heading}s'.format(heading=index+2),
            'words': bucket
        }
        for index, bucket in enumerate(buckets)
    ]

    return template(
        os.path.dirname(__file__) + '/index.tpl',
        starts_with=starts_with,
        ends_with=ends_with,
        contains=contains,
        focus=focus,
        buckets=template_buckets
    )


if __name__=='__main__':
    run(host='localhost', port=1024, debug=True)
