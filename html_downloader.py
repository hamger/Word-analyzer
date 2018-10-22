#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
from urllib import request as req
from urllib.parse import quote

def download(url):
    if url is None:
        return None
    url_ = quote(url, safe=string.printable)
    response = req.urlopen(url_)
    if response.getcode() != 200:
        return None

    return response.read()