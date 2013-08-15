# -*- coding: utf-8 -*-

import sys
import re
import time
import ptt

reader = ptt.PttReader()
if not reader.login():
    exit()

print '您想去哪個板'
board_name = sys.stdin.readline().strip()
reader.go_to_board(board_name)

print '想查什麼關鍵字'
keyword = sys.stdin.readline().strip()

print '從最新的100篇文章裡面找好嗎 (Y/n)'
find100 = sys.stdin.readline().strip().lower()
if not find100.startswith('n'):
    end_pos = reader.latest_article_number()
    begin_pos = end_pos - 100 + 1
else:
    print '從第幾篇開始找'
    begin_pos = sys.stdin.readline().strip()
    print '一直找到哪一篇'
    end_pos = sys.stdin.readline().strip()
    begin_pos = int(begin_pos)
    end_pos = int(end_pos)

for pos in range(begin_pos, end_pos + 1):
    print pos
