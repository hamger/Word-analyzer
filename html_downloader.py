#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
import urllib.request
from urllib.parse import quote

def download(url):
    if url is None:
        return None
    url_ = quote(url, safe=string.printable)

    req = urllib.request.Request(url_)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3595.2 Safari/537.36')
    response = urllib.request.urlopen(req)
    if response.getcode() != 200:
        return None

    return response.read()