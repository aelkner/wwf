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
    form, focus, opts, filters = {}, '', '', []
    for opt, field in [
        ('s', 'starts_with'),
        ('e', 'ends_with'),
        ('c', 'contains'),
    ]:
        form[field] = '' if not request.forms else request.forms.get(field, '')
        if form[field]:
            opts += opt
            filters.append(form[field])
            if not focus:
                focus = field

    if not filters:
        filtered_words = []
        focus = 'starts_with'
    else:
        filtered_words = utils.filter_words(words, opts, filters)
    buckets = utils.build_buckets(filtered_words)

    if buckets:
        index, total = 0, 0
        while True:
            total += len(buckets[index])
            if total > 15000:
                break
            index += 1
            if index >= len(buckets):
                break
        buckets = buckets[:index]

    template_buckets = [
        {
            'heading': '{heading}s'.format(heading=index+2),
            'words': bucket,
        }
        for index, bucket in enumerate(buckets)
    ]

    return template(
        os.path.dirname(__file__) + '/index.tpl',
        form=form,
        focus=focus,
        buckets=template_buckets
    )


if __name__=='__main__':
    run(host='localhost', port=1024, debug=True)
