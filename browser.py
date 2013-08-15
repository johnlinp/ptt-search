# -*- coding: utf-8 -*-

import re, json
import time
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

class Browser:
    def __init__(self):
        self._br = mechanize.Browser()
        self._set_cookie_jar()
        self._set_options()

    def _set_cookie_jar(self):
        cj = cookielib.LWPCookieJar()
        self._br.set_cookiejar(cj)

    def _set_options(self):
        self._br.set_handle_equiv(True)
        self._br.set_handle_redirect(True)
        self._br.set_handle_referer(True)
        self._br.set_handle_robots(False)
        self._br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self._br.addheaders = [('User-agent', 
                                '''Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) 
                                Gecko/2008071615 
                                Fedora/3.0.1-1.fc9 
                                Firefox/3.0.1''')]

    def _get_page_soup(self, url):
        try:
            page = self._br.open(url)
        except:
            return None
        content = page.read()
        content = re.sub('/ >', '/>', content) # workaround for strange BeautifulSoup...
        soup = BeautifulSoup(content)
        return soup

class Ptt(Browser):
    def go_to_board(self, board_name):
        self._articles = {}
        url = 'http://www.ptt.cc/bbs/%s/index.html' % board_name
        soup = self._get_page_soup(url)
        if not soup:
            return False
        self._board_head_soup = soup
        self._put_article(soup)
        return True

    def latest_article_number(self):
        return max(self._articles.keys())

    def get_article_content(self, article_num):
        while article_num not in self._articles:
            self._grab_prev_page()
        url = self._articles[article_num]
        soup = self._get_page_soup(url)
        if not soup:
            return ''
        content = soup.find('div', {'id': 'mainContent'})
        return str(content)

    def _grab_prev_page(self):
        links = self._board_head_soup.findAll('a')
        url = None
        for link in links:
            if str(link.string) == '上一頁' and 'index' in link['href']:
                url = link['href']
                break
        assert url
        soup = self._get_page_soup(url)
        self._board_head_soup = soup
        self._put_article(soup)

    def _put_article(self, soup):
        if not soup:
            return None
        dl = soup.find('dl')
        rows = dl.findAll('tr')
        for row in rows:
            cells = row.findAll('td')
            num = int(cells[0].string)
            link = cells[-1].find('a')['href']
            self._articles[num] = link

