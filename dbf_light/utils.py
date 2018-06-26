# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import codecs


def bytes_to_int(val):
    return int(codecs.encode(val, 'hex'), 16)
