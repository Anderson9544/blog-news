import datetime, html, re, urllib.parse
import feedparser

NORMAL = ["네이버 검색", "검색 엔진", "구글 검색", "SEO 최적화", "다음 포털", "티스토리", "빙 검색", "애드포스트", "구글 블로그 스팟", "애드센스", "데이블", "카카오", "애드핏", "AIO", "AEO", "GEO", "구글 블로그", "워드프레스"]   # 일반 검색 (기사 어디든 포함)
STRICT = ["네이버 블로그", "블로그"]                    # 제목 맨 앞에 있는 기사만
MAX_PER_QUERY = 5

def feed_url(q):
    return ("https://news.google.com/rss/search?q="
            + urllib.parse.quote(q + " when:1d")
            + "&hl=ko&gl=KR&ceid=KR:ko")

# 제목 앞의 [단독], (종합) 같은 말머리 제거용
TAG = re.compile(r'^(\s*[\[\(<「『][^\]\)>」』]*[\]\)>」』])+\s*')

jobs = [(k, False) for k in NORMAL] + [(k, True) for k in STRICT]

seen, sections = set(), []
for kw, strict in jobs:
    q = f'intitle:"{kw}"' if strict else f'"{kw}"'
    items = []
    for e in feedparser.parse(feed_url(q)).entries:
        if strict:
            title = TAG.sub("", e.title)
            if not title.lower().startswith(kw.lower()):
                continue
        if e.link in seen:
            continue
        seen.add(e.link)
        items.append(f'<li><a href="{html.escape(e.link)}">{html.escape(e.title)}</a></li>')
        if len(items) >= MAX_PER_QUERY:
            break
    if items:
        sections.append(f"<h2>{html.escape(kw)}</h2><ul>{''.join(items)}</ul>")

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
