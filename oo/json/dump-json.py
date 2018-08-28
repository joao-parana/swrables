#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Para invocar faça, por exemplo: ./dump-json.py first-iteraction.json
#

import json
import sys

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    print args

    FILE_NAME = 'first-iteraction.json'
    if len(args) > 0:
        FILE_NAME = args[0].strip()

    with open(FILE_NAME, 'r') as handle:
        parsed = json.load(handle)

    print json.dumps(parsed, indent=4, sort_keys=True)

if __name__ == "__main__" :
    main()
