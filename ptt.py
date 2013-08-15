# -*- coding: utf-8 -*-

import os, sys, re
import telnetlib
import time
import config

class PttReader:
    def __init__(self):
        self._username = config.username
        self._password = config.password
        self._quiet_mode = config.quiet_mode
        self._log = None
        if config.debug_log:
            self._log = open(config.debug_log, 'w')

        while True:
            self._tn = telnetlib.Telnet('ptt.cc')
            which, trash, trash = self._expect([self._utf8_to_big5('註冊'), self._utf8_to_big5('系統過載, 請稍後再來')])
            if which == 0:
                break
            if not self._quiet_mode:
                print '系統過載啦 自動休息十秒鐘'
            time.sleep(10)

    def login(self):
        self._tn.write(self._username + ',\r')
        self._expect([self._utf8_to_big5('密碼')])
        self._tn.write(self._password + '\r')
        which, trash, trash = self._expect(['請按任意鍵繼續', '您想刪除其他重複登入的連線嗎？', self._utf8_to_big5('有無輸入錯誤。')])
        if which == 0:
            self._tn.write('\r')
        elif which == 1:
            self._tn.write('n\r')
            self._expect(['請按任意鍵繼續'])
            self._tn.write('\r')
        else:
            if not self._quiet_mode:
                print '帳號密碼好像錯囉'
                return False
        self._expect(['離開，再見'])
        if not self._quiet_mode:
            print '以%s順利登入了' % self._username
        return True

    def go_to_board(self, board):
        self._tn.write('s' + board + '\r')
        which, trash, read = self._expect(['進板畫面', '請按任意鍵繼續'])
        if which == 1:
            self._tn.write('\r')
            trash, trash, read = self._expect(['進板畫面'])
        self._find_latest_article_number(read)
        if not self._quiet_mode:
            print '成功進入%s板了' % board

    def latest_article_number(self):
        return self._latest_article_number

    def _find_latest_article_number(self, read):
        lines = read.split('\n')
        self._latest_article_number = -1
        for line in lines:
            mo = re.match('^\s*(\d+)', line)
            if mo:
                battle = int(mo.group(1)) + 1 # the cursor
                if battle > self._latest_article_number:
                    self._latest_article_number = battle

    def _expect(self, to_expect):
        real = self._tn.expect(to_expect, 5)
        if self._log:
            self._log.write(real[2])
            self._log.write('\n\n================================\n\n')
        if real[0] == -1:
            assert False
        return real

    def _utf8_to_big5(self, utf8):
        return utf8.decode('utf8').encode('big5')

