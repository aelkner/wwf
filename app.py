#!/usr/bin/env python
import os
import sys

import utils


def get_command_line_args():
    def usage():
        print('Usage: app.py [s][e][c] filter [additional filters] ')
        sys.exit()

    try:
        opts = sys.argv[1]
        filters = sys.argv[2:]
    except:
        usage()
    if len(opts) != len(filters):
        usage()
    for opt in opts:
        if opt not in 'sec':
            usage()
    return opts, filters


def main():
    """
    utils.save_wwf_words()
    return
    """
    opts, filters = get_command_line_args()
    words = utils.load_words()
    words = utils.filter_words(words, opts, filters)
    buckets = utils.build_buckets(words)
    utils.print_buckets(buckets)


if __name__=='__main__':
    main()
