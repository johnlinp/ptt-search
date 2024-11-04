#!/usr/bin/env python3

import sys
import argparse
import logging
import re
import json
import requests
import urllib.parse
from bs4 import BeautifulSoup


class PttSearch:
    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description='PTT Search - 免登入 PTT 搜尋')

        parser.add_argument('--board', '-b', help='看板名稱')
        parser.add_argument('--keyword', '-k', help='搜尋關鍵字')
        parser.add_argument('--author', '-a', help='搜尋作者')
        parser.add_argument('--verbose', '-v', action='store_true', help='除錯模式')

        return parser.parse_args()

    @staticmethod
    def run(args):
        PttSearch._config_logging(args.verbose)

        PttSearch._check_args(args)

        logging.debug('check args done')

        post_urls = PttSearch._search(args.board, args.keyword, args.author)

        for post_url in post_urls:
            print(post_url)

        logging.debug('shutting down')

    @staticmethod
    def _search(board, keyword, author):
        PttSearch._check_board_exists(board)

        first_page_url = PttSearch._generate_search_url(board, keyword, author)
        logging.debug(f'start searching with the url: {first_page_url}')

        all_post_urls = []
        post_urls, next_page_url = PttSearch._search_by_url(first_page_url)
        all_post_urls.extend(post_urls)
        while next_page_url:
            post_urls, next_page_url = PttSearch._search_by_url(next_page_url)
            all_post_urls.extend(post_urls)
        return all_post_urls

    @staticmethod
    def _check_board_exists(board):
        board_url = PttSearch._generate_board_url(board)
        try:
            PttSearch._fetch_page(board_url)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise Error(f'看板 {board} 不存在')
            else:
                raise e

    @staticmethod
    def _generate_board_url(board):
        path = PttSearch._generate_board_url_path(board)
        return f'{PttSearch._PTT_BASE_URL}/{path}'

    @staticmethod
    def _generate_board_url_path(board):
        path_components = [
            'bbs',
            board
        ]
        return '/'.join(path_components)

    @staticmethod
    def _generate_search_url(board, keyword, author):
        path = PttSearch._generate_search_url_path(board)
        query_params = PttSearch._generate_search_url_query_params(keyword, author)
        return f'{PttSearch._PTT_BASE_URL}/{path}?{query_params}'

    @staticmethod
    def _generate_search_url_path(board):
        path_components = [
            'bbs',
            board,
            'search'
        ]
        return '/'.join(path_components)

    @staticmethod
    def _generate_search_url_query_params(keyword, author):
        search_queries = []
        if keyword:
            search_queries.append(keyword)
        if author:
            search_queries.append(f'author:{author}')
        return urllib.parse.urlencode({
            'q': ' '.join(search_queries)
        })

    @staticmethod
    def _search_by_url(url):
        content = PttSearch._fetch_page(url)
        soup = BeautifulSoup(content, 'html.parser')
        post_urls = PttSearch._extract_post_urls(soup)
        next_page_url = PttSearch._extract_next_page_url(soup)
        return post_urls, next_page_url

    @staticmethod
    def _extract_post_urls(soup):
        post_urls = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            logging.debug(f'found href: {href}')
            if PttSearch._is_post_href(href):
                post_urls.append(f'{PttSearch._PTT_BASE_URL}{href}')
        return post_urls

    @staticmethod
    def _extract_next_page_url(soup):
        next_page_button = soup.find('a', string=re.compile('上頁'))
        logging.debug(f'next_page_button: {next_page_button}')
        if 'disabled' in next_page_button['class']:
            return None
        href = next_page_button['href']
        return f'{PttSearch._PTT_BASE_URL}{href}'

    @staticmethod
    def _is_post_href(href):
        return bool(re.match(r'.*/M\.\w+\.A\.\w+\.html', href))

    @staticmethod
    def _fetch_page(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @staticmethod
    def _check_args(args):
        if not args.board:
            raise Error('請使用 --board 參數提供看板名稱')
        if not args.keyword and not args.author:
            raise Error('請至少使用 --keyword 與 --author 其中一個參數提供搜尋條件')

    @staticmethod
    def _config_logging(verbose):
        log_level = logging.DEBUG if verbose else logging.INFO
        log_format = '%(levelname)s: %(message)s'
        logging.basicConfig(level=log_level, format=log_format)

    _PTT_BASE_URL = 'https://www.ptt.cc'


class Error(Exception):
    pass


def main():
    args = PttSearch.parse_args()
    PttSearch.run(args)


if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except Error as e:
        logging.error(e)
        sys.exit(1)
