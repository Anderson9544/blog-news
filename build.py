import datetime, html, urllib.parse
import feedparser

QUERIES = ["네이버 블로그", "네이버", "티스토리", "SEO", "다음", "구글", "애드포스트", "구글블로그스팟", "애드센스", "데이블", "카카오", "애드핏", "AIO", "AEO", "GEO", "구글블로그", "블로거", "검색엔진최적화", "워드프레스"]
MAX_PER_QUERY = 5

def feed_url(q):
    return ("https://news.google.com/rss/search?q="
            + urllib.parse.quote(q + " when:1d")
            + "&hl=ko&gl=KR&ceid=KR:ko")

seen, sections = set(), []
for q in QUERIES:
    items = []
    for e in feedparser.parse(feed_url(q)).entries:
        if e.link in seen:
            continue
        seen.add(e.link)
        items.append(f'<li><a href="{html.escape(e.link)}">{html.escape(e.title)}</a></li>')
        if len(items) >= MAX_PER_QUERY:
            break
    if items:
        sections.append(f"<h2>{html.escape(q)}</h2><ul>{''.join(items)}</ul>")

kst = datetime.timezone(datetime.timedelta(hours=9))
today = datetime.datetime.now(kst).strftime("%Y-%m-%d")
page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta property="og:title" content="오늘의 블로그 뉴스 ({today})">
<meta property="og:description" content="블로그·애드센스·SEO 관련 최신 뉴스 모음">
<title>오늘의 블로그 뉴스</title></head>
<body style="max-width:720px;margin:auto;padding:16px;font-family:sans-serif">
<h1>📰 오늘의 블로그 뉴스 ({today})</h1>
{''.join(sections)}
</body></html>"""
open("index.html", "w", encoding="utf-8").write(page)
