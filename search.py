# -*- coding: utf-8 -*-

import sys
import re
import browser

ptt = browser.Ptt()

success = False
print '您想去哪個板'
while not success:
    board_name = sys.stdin.readline().strip()
    success = ptt.go_to_board(board_name)
    if not success:
        print '板名怪怪的 請重新輸入'

print '想查什麼關鍵字'
keyword = sys.stdin.readline().strip()

print '從最新的100篇文章裡面找好嗎 (Y/n)'
find100 = sys.stdin.readline().strip().lower()
if not find100.startswith('n'):
    end_pos = ptt.latest_article_number()
    begin_pos = end_pos - 100 + 1
else:
    print '從第幾篇開始找'
    begin_pos = sys.stdin.readline().strip()
    print '一直找到哪一篇'
    end_pos = sys.stdin.readline().strip()
    begin_pos = int(begin_pos)
    end_pos = int(end_pos)

found = []
for pos in range(begin_pos, end_pos + 1):
    report = '\r正在找第%s篇' % pos
    if found:
        joins = ' '.join(found[:5])
        if len(found) > 5:
            joins += '...'
        report += ' 已經在第%s篇找到' % joins
    print report,
    sys.stdout.flush()
    content = ptt.get_article_content(pos)
    if keyword in content:
        found.append(str(pos))

print
print
print '搜尋結果:', ' '.join(found)


