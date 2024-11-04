# PTT Search - 免登入 PTT 搜尋

簡單的 PTT 文章搜尋工具。只要提供 PTT 看板名稱與搜尋條件，就可以幫你列出符合條件的所有 PTT 文章網址。


## 安裝

```
$ pip3 install -r requirements.txt
```

## 使用範例

### 使用關鍵字搜尋

```
$ python3 ptt-search.py --board joke --keyword 蠶寶寶
https://www.ptt.cc/bbs/joke/M.1689651901.A.EE3.html
https://www.ptt.cc/bbs/joke/M.1689421997.A.230.html
https://www.ptt.cc/bbs/joke/M.1664421509.A.548.html
https://www.ptt.cc/bbs/joke/M.1620767011.A.20E.html
https://www.ptt.cc/bbs/joke/M.1620302430.A.D88.html
https://www.ptt.cc/bbs/joke/M.1620131848.A.760.html
https://www.ptt.cc/bbs/joke/M.1620049789.A.35D.html
https://www.ptt.cc/bbs/joke/M.1620041044.A.D88.html
https://www.ptt.cc/bbs/joke/M.1620041032.A.642.html
https://www.ptt.cc/bbs/joke/M.1620032053.A.2AC.html
https://www.ptt.cc/bbs/joke/M.1620016751.A.5A0.html
...
```

### 使用作者搜尋

```
$ python3 ptt-search.py --board joke --author johnlinp
https://www.ptt.cc/bbs/joke/M.1702161111.A.7E0.html
https://www.ptt.cc/bbs/joke/M.1693812531.A.E83.html
https://www.ptt.cc/bbs/joke/M.1678563314.A.E4F.html
https://www.ptt.cc/bbs/joke/M.1666369465.A.66C.html
https://www.ptt.cc/bbs/joke/M.1662180852.A.548.html
https://www.ptt.cc/bbs/joke/M.1660868899.A.AA3.html
https://www.ptt.cc/bbs/joke/M.1651538189.A.1A8.html
https://www.ptt.cc/bbs/joke/M.1647130321.A.20B.html
https://www.ptt.cc/bbs/joke/M.1646259858.A.873.html
...
```
