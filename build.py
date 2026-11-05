import os, re, html, json, shutil, hashlib, datetime
from articles1 import A, REF
from articles2 import B
from articles3 import C
ARTS = A + B + C
SITE = os.environ.get("SITE_URL", "https://example.com").rstrip("/")
NAME = "VPS на практике"
TAG = "Практические инструкции по VPS: настройка, боты, сайты, WireGuard, Docker"
OUT = "docs"
TODAY = datetime.date.today().isoformat()
KEY = hashlib.sha1(SITE.encode()).hexdigest()[:32]
e = html.escape

CSS = """
:root{--bg:#fff;--fg:#1a1d21;--mut:#5b6470;--line:#e3e7ec;--acc:#0b6bcb;--card:#f5f7fa;--code:#0f1720;--codefg:#e6edf3}
@media(prefers-color-scheme:dark){:root{--bg:#0f1318;--fg:#e6e9ee;--mut:#9aa5b1;--line:#252c35;--acc:#5aa9ff;--card:#171d25}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.7 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
a{color:var(--acc)}header,main,footer{max-width:760px;margin:0 auto;padding:0 16px}
header{display:flex;justify-content:space-between;align-items:center;padding-top:14px;padding-bottom:14px;border-bottom:1px solid var(--line);flex-wrap:wrap;gap:8px}
.logo{font-weight:700;text-decoration:none;color:var(--fg)}nav a{margin-left:14px;text-decoration:none}
h1{font-size:2rem;line-height:1.25;margin:1.2em 0 .4em}h2{font-size:1.4rem;margin:1.8em 0 .5em;line-height:1.3}
pre{background:var(--code);color:var(--codefg);padding:14px;border-radius:8px;overflow:auto;font-size:.88rem;line-height:1.5}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.92em}p code,li code,td code{background:var(--card);padding:1px 5px;border-radius:4px}
table{border-collapse:collapse;width:100%;display:block;overflow-x:auto;margin:1em 0}td,th{border:1px solid var(--line);padding:8px 10px;text-align:left;font-size:.94rem}th{background:var(--card)}
.meta{color:var(--mut);font-size:.9rem}.toc{background:var(--card);border-radius:10px;padding:12px 18px;margin:1.2em 0}.toc ol{margin:.3em 0;padding-left:20px}
.cta{border:1px solid var(--acc);border-radius:12px;padding:16px 18px;margin:1.8em 0;background:var(--card)}.cta p{margin:.4em 0}.cta small{display:block;color:var(--mut);margin-top:8px}
.btn{display:inline-block;background:var(--acc);color:#fff;padding:10px 18px;border-radius:8px;text-decoration:none;font-weight:600;margin-top:6px}
.cards{display:grid;gap:14px;margin:1.2em 0}.card{border:1px solid var(--line);border-radius:12px;padding:14px 16px;text-decoration:none;color:var(--fg);display:block}.card:hover{border-color:var(--acc)}.card b{display:block;font-size:1.05rem}.card span{color:var(--mut);font-size:.92rem}
footer{border-top:1px solid var(--line);margin-top:3em;padding-top:18px;padding-bottom:30px;color:var(--mut);font-size:.88rem}
.crumbs{font-size:.88rem;color:var(--mut);margin-top:14px}details{border:1px solid var(--line);border-radius:8px;padding:10px 14px;margin:8px 0}summary{cursor:pointer;font-weight:600}
"""

def slugify(t): return re.sub(r'[^a-z0-9а-я]+','-',t.lower()).strip('-')

def add_toc(body):
    heads=[]
    def rep(m):
        t=re.sub('<[^>]+>','',m.group(1)); i="s-"+str(len(heads)+1); heads.append((i,t))
        return f'<h2 id="{i}">{m.group(1)}</h2>'
    body=re.sub(r'<h2>(.*?)</h2>',rep,body)
    toc='<nav class="toc" aria-label="Содержание"><b>Содержание</b><ol>'+''.join(f'<li><a href="#{i}">{e(t)}</a></li>' for i,t in heads)+'</ol></nav>'
    return body,toc

def page(path,title,desc,body,canonical,extra_head="",og_type="website"):
    url=SITE+canonical
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta property="og:type" content="{og_type}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="{NAME}">
<meta name="yandex-verification" content="a39d48587ac618b0" /><meta name="google-site-verification" content="Yp9jwHr4COqJ1m2GRLwet1UMlz9AoIvd9c-SAXJsfBM" /><meta name="twitter:card" content="summary"><link rel="alternate" type="application/rss+xml" title="{NAME}" href="{SITE}/rss.xml">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%230b6bcb'/%3E%3Ctext x='32' y='43' font-size='30' text-anchor='middle' fill='white' font-family='monospace'%3E%3E_%3C/text%3E%3C/svg%3E">
<style>{CSS}</style>{extra_head}</head><body>
<header><a class="logo" href="/">▸ {NAME}</a><nav><a href="/articles/">Статьи</a><a href="/about/">О сайте</a></nav></header>
<main>{body}</main>
<footer><p>{NAME} — {e(TAG)}.</p><p>Раскрытие: на сайте есть партнёрские ссылки на хостинг Aeza. Они не увеличивают цену для вас, но приносят автору вознаграждение. <a href="/about/">Подробнее</a>.</p><p>© {datetime.date.today().year}</p></footer>
</body></html>'''

def w(path,content):
    p=os.path.join(OUT,path.lstrip('/'));os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,'w',encoding='utf-8').write(content)

def jld(o): return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>'

shutil.rmtree(OUT,ignore_errors=True)
ARTS.sort(key=lambda a:a['slug'])
order=["kak-vybrat-vps","nastroika-ubuntu-vps","vps-vs-vds-vs-hosting","aeza-obzor","telegram-bot-na-vps","sajt-na-vps-nginx-ssl","wireguard-na-vps","docker-na-vps","minecraft-server-na-vps"]
ARTS.sort(key=lambda a:order.index(a['slug']))
bymap={a['slug']:a for a in ARTS}

def card(a): return f'<a class="card" href="/articles/{a["slug"]}/"><b>{e(a["h1"])}</b><span>{e(a["desc"])}</span></a>'

for a in ARTS:
    body,toc=add_toc(a['body'])
    words=len(re.sub('<[^>]+>',' ',a['body']).split()); mins=max(2,round(words/180))
    related=[x for x in ARTS if x['slug']!=a['slug']]
    # related: next 3 in order after current
    i=order.index(a['slug']); rel=[bymap[order[(i+k)%len(order)]] for k in (1,2,3)]
    faq=''.join(f'<details><summary>{e(q)}</summary><p>{e(an)}</p></details>' for q,an in a['faq'])
    url=f"{SITE}/articles/{a['slug']}/"
    ld=[
     {"@context":"https://schema.org","@type":"Article","headline":a['h1'],"description":a['desc'],"inLanguage":"ru","datePublished":a['date'],"dateModified":TODAY,"mainEntityOfPage":url,"author":{"@type":"Organization","name":NAME,"url":SITE},"publisher":{"@type":"Organization","name":NAME,"url":SITE},"keywords":a['kw']},
     {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":an}} for q,an in a['faq']]},
     {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Главная","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Статьи","item":SITE+"/articles/"},{"@type":"ListItem","position":3,"name":a['h1'],"item":url}]}]
    html_body=f'''<div class="crumbs"><a href="/">Главная</a> › <a href="/articles/">Статьи</a></div>
<article><h1>{e(a['h1'])}</h1><p class="meta">Обновлено: {TODAY} · чтение ~{mins} мин</p>{toc}{body}
<h2>Частые вопросы</h2>{faq}</article>
<h2>Читайте также</h2><div class="cards">{''.join(card(x) for x in rel)}</div>'''
    w(f"articles/{a['slug']}/index.html",page(None,a['title'],a['desc'],html_body,f"/articles/{a['slug']}/",''.join(jld(x) for x in ld),"article"))

# index
home=f'''<h1>VPS без боли: пошаговые инструкции</h1>
<p>Здесь собраны проверенные пошаговые гайды по VPS: как выбрать сервер, защитить его, запустить Telegram-бота, сайт, WireGuard, Docker и Minecraft. Только рабочие команды и объяснения простым языком.</p>
<div class="cta"><strong>Нужен сервер для практики?</strong><p>Все инструкции подойдут для любого VPS на Ubuntu. Я использую и рекомендую Aeza — актуальные тарифы смотрите на сайте.</p><a class="btn" href="{REF}" rel="sponsored nofollow noopener" target="_blank">Тарифы Aeza →</a><small>Партнёрская ссылка</small></div>
<h2>Начните отсюда</h2><div class="cards">{''.join(card(bymap[s]) for s in order[:4])}</div>
<h2>Практические проекты</h2><div class="cards">{''.join(card(bymap[s]) for s in order[4:])}</div>'''
w("index.html",page(None,f"{NAME} — инструкции по VPS: настройка, боты, сайты, WireGuard","Пошаговые инструкции по VPS на Ubuntu: как выбрать сервер, защитить его, запустить Telegram-бота, сайт на Nginx, WireGuard, Docker и Minecraft.",home,"/",jld({"@context":"https://schema.org","@type":"WebSite","name":NAME,"url":SITE+"/","inLanguage":"ru"})))
w("articles/index.html",page(None,f"Все статьи — {NAME}","Каталог инструкций по VPS: выбор, настройка, безопасность, боты, сайты, VPN, Docker и игровые серверы.",f'<h1>Все статьи</h1><div class="cards">{"".join(card(a) for a in ARTS)}</div>',"/articles/"))
about=f'''<h1>О сайте и раскрытие партнёрских отношений</h1>
<p>{NAME} — независимый справочник практических инструкций по администрированию VPS. Все команды проверяйте на тестовом сервере перед использованием в работе.</p>
<h2>Партнёрские ссылки</h2><p>Часть ссылок на хостинг Aeza содержит реферальный код. Если вы зарегистрируетесь по такой ссылке и закажете услугу, автор сайта может получить вознаграждение. Для вас цена не меняется. Партнёрские ссылки помечены атрибутами <code>rel="sponsored nofollow"</code>.</p>
<h2>Ограничения</h2><p>Тарифы, цены и характеристики хостеров меняются. Актуальную информацию всегда сверяйте на официальном сайте поставщика. Материалы носят информационный характер.</p>
<h2>Реклама</h2><p>Сайт содержит рекламу партнёрской программы хостинга Aeza.</p>'''
w("about/index.html",page(None,f"О сайте — {NAME}","О проекте, раскрытие партнёрских ссылок и ограничения ответственности.",about,"/about/"))
w("404.html",page(None,f"Страница не найдена — {NAME}","Страница не найдена.","<h1>404 — страница не найдена</h1><p><a href='/'>На главную</a> или <a href='/articles/'>к статьям</a>.</p>","/404.html").replace('index,follow','noindex'))

urls=[("/",TODAY,"1.0"),("/articles/",TODAY,"0.8"),("/about/",TODAY,"0.3")]+[(f"/articles/{a['slug']}/",TODAY,"0.9") for a in ARTS]
w("sitemap.xml",'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod><priority>{p}</priority></url>' for u,d,p in urls)+'</urlset>')
w("robots.txt",f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
w("rss.xml",'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>'+NAME+'</title><link>'+SITE+'/</link><description>'+e(TAG)+'</description><language>ru</language>'+''.join(f'<item><title>{e(a["h1"])}</title><link>{SITE}/articles/{a["slug"]}/</link><guid>{SITE}/articles/{a["slug"]}/</guid><description>{e(a["desc"])}</description></item>' for a in ARTS)+'</channel></rss>')
w(f"{KEY}.txt",KEY)
open("indexnow.json","w").write(json.dumps({"host":SITE.split('//')[1],"key":KEY,"keyLocation":f"{SITE}/{KEY}.txt","urlList":[SITE+u for u,_,_ in urls]},ensure_ascii=False))
print("built",len(ARTS),"articles; key",KEY)
