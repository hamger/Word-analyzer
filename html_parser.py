#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import re


def _get_data(soup):
    res_data = {
        'phonetic': [],
        'meaning': [],
    }
    try:
        phonetic_node = soup.find_all('span', class_='phonetic')
        for node in phonetic_node:
            res_data['phonetic'].append(node.get_text())
    except:
        pass

    try:
        meaning_node = soup.find(
            "div", class_="trans-container").find('ul').find_all('li')
        for node in meaning_node:
            res_data['meaning'].append(node.get_text()) 
    except:
        pass

    return res_data


def prase(html_cont):
    if html_cont is None:
        return
    soup = bs(html_cont, 'html.parser', from_encoding='utf-8')
    data = _get_data(soup)
    return data
