#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree as ET
import html
from datetime import datetime

desktop_path = "/mnt/c/Users/ben82/Desktop/"
today = datetime.now().strftime("%Y-%m-%d")

def fetch_rss(url, category):
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            content = response.read().decode('utf-8')
        
        root = ET.fromstring(content)
        channel = root.find('channel')
        if channel is None:
            return f"【{category}】無法解析 XML\n\n"
        
        item = channel.find('item')
        if item is None:
            return f"【{category}】無內容\n\n"
        
        title = ""
        desc = ""
        
        for child in item:
            if child.tag == 'title':
                title = html.unescape(child.text or "")
            elif child.tag in ('description', 'summary'):
                desc = html.unescape(child.text or "")
        
        # 清除 HTML 標籤
        clean_desc = ""
        inside_tag = False
        for c in desc:
            if c == '<':
                inside_tag = True
            elif c == '>':
                inside_tag = False
            elif not inside_tag:
                clean_desc += c
        clean_desc = clean_desc.strip()[:300]
        
        return f"【{category}】\n標題：{title}\n摘要：{clean_desc}...\n\n"
    except Exception as e:
        return f"【{category}】無法取得：{str(e)}\n\n"

# 收集各類文章
articles = f"📚 每日教學文章 {today}\n{'='*40}\n\n"

# 理財 - Budgets Are Sexy (個人理財教學)
articles += fetch_rss("https://feeds.feedburner.com/BudgetsAreSexy", "💰 理財")

# 運動 - StrongLifts (健身教學)
articles += fetch_rss("https://feeds.feedburner.com/StrongLifts", "🏃 運動")

# 日語 - NHK 日本語學習
articles += fetch_rss("https://www.nhk.or.jp/rss/news/cat0.xml", "🇯🇵 日語")

# 英語 - BBC Learning English Podcast
articles += fetch_rss("https://podcasts.files.bbci.co.uk/p02pc9tn.rss", "🇬🇧 英語")

articles += "="*40 + "\n由 Hermes Agent 自動生成"

# 儲存到桌面
output_file = f"{desktop_path}每日文章_{today}.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(articles)

print(articles)
