# -*- coding: utf-8 -*-

import requests as web
import bs4
import csv

from ipdb import set_trace
import re

def get_text(list_keywd):

    print(list_keywd)

    resp = web.get('https://news.infoseek.co.jp/search?type=article&num=10&q=' + '　'.join(list_keywd))

    resp.raise_for_status()

    # 取得したHTMLをパースする
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    # 検索結果のタイトルとリンクを取得
    link_elem01 = soup.select('.article-list > li > a')

    # 1番上の記事URLを取得
    _url_text = link_elem01[0].get('href')
    url_text = "https://news.infoseek.co.jp"+_url_text
    #url_text = 'https://news.infoseek.co.jp/article/sankein_wst1905180016/'

    # 記事の情報を取得
    resp = web.get(url_text)
    resp.raise_for_status()

    # 取得したHTMLをパースする
    soup = bs4.BeautifulSoup(resp.text, "html.parser")

    corpus = []


    # テキストを取得
    all_p_soup = soup.find(class_="topic-detail")
    all_p_soup_ = all_p_soup.find(class_="topic-detail__text")

    for p_tag in all_p_soup_.find_all('p'):
        text = "".join(p_tag.text.strip().split(" "))
        if len(text) == 0:
            continue
        # e.g. [注釈9] -> ''
        text = re.sub(r"\[注釈[0-9]+\]", "", text.replace('\n',''))
        # e.g. [20] -> ''
        text = re.sub(r"\[[0-9]+\]", "", text.replace('　',''))
        corpus.append(text)

    __text = ""
    for i in range(len(corpus)):
        __text += corpus[i]
    return __text

