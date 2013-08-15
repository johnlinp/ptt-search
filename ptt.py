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
            which = self._expect([self._utf8_to_big5('註冊'), self._utf8_to_big5('系統過載, 請稍後再來')], False)
            if which == 0:
                break
            if not self._quiet_mode:
                print '系統過載啦 自動休息十秒鐘'
            time.sleep(10)

    def login(self):
        self._tn.write(self._username + ',\r')
        self._expect([self._utf8_to_big5('密碼')], False)
        self._tn.write(self._password + '\r')
        which = self._expect(['請按任意鍵繼續', '您想刪除其他重複登入的連線嗎？', self._utf8_to_big5('有無輸入錯誤。')])
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
        self._expect(['請按任意鍵繼續'])
        self._tn.write('\r')
        self._expect(['進板畫面'])
        if not self._quiet_mode:
            print '成功進入%s板了' % board

    def latest_article_number(self):
        return 1000

    def _expect(self, to_expect, is_utf8=True):
        q = self._tn.expect(to_expect, 5)
        if q[0] == -1:
            if self._log:
                self._log.write('========= expect error =========\n')
                self._log.write(q[2])
                self._log.write('================================\n')
            assert False
        return q[0]

    def _utf8_to_big5(self, utf8):
        return utf8.decode('utf8').encode('big5')

