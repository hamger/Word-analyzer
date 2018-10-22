#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import re


def _get_data(soup):
    res_data = {}

    phonetic_node = soup.find('span', class_='phonetic')
    for index, node in enumerate(phonetic_node):
        res_data['phonetic_' + index] = node.get_text()

    meaning_node = soup.find(
        "div", class_="trans-container").find('ul').find_all('li')
    for index, node in enumerate(meaning_node):
        res_data['meaning_' + index] = node.get_text()

    return res_data


def parse(html_cont):
    if html_cont is None:
        return
    soup = bs(html_cont, 'html.parser', from_encoding='utf-8')
    data = _get_data(soup)
    return data
