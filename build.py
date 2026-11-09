import os, re, html, json, shutil, hashlib, datetime
from articles1 import A, REF
from articles2 import B
from articles3 import C
from articles4 import D
from articles5 import E
ARTS = A + B + C + D + E
SITE = os.environ.get("SITE_URL", "https://vps.lainos.online").rstrip("/")
NAME = "VPS на практике"
TAG = "Практические инструкции по VPS: настройка, боты, сайты, WireGuard, Docker"
OUT = "docs"
TODAY = "2026-11-09"
METRICA = 114144631
BOT_SITE = "https://dolepp.github.io/bot-launch/"
FLOW_SITE = "https://dolepp.github.io/automation-lab/"
KEY = hashlib.sha1(SITE.encode()).hexdigest()[:32]
e = html.escape
YANDEX = '<meta name="yandex-verification" content="a39d48587ac618b0" />'
GOOGLE = '<meta name="google-site-verification" content="Yp9jwHr4COqJ1m2GRLwet1UMlz9AoIvd9c-SAXJsfBM" />'

# slug: (рубрика, уровень, иконка)
META = {
 "kak-vybrat-vps": ("Выбор", "Новичок", "🧭"),
 "nastroika-ubuntu-vps": ("Безопасность", "Новичок", "🛡️"),
 "podklyuchenie-k-vps-po-ssh": ("Основы", "Новичок", "🔑"),
 "vps-vs-vds-vs-hosting": ("Основы", "Новичок", "⚖️"),
 "aeza-obzor": ("Обзор", "Новичок", "⭐"),
 "telegram-bot-na-vps": ("Боты", "Новичок", "🤖"),
 "sajt-na-vps-nginx-ssl": ("Сайты", "Средний", "🌐"),
 "wordpress-na-vps": ("Сайты", "Средний", "📝"),
 "fastapi-na-vps": ("Разработка", "Средний", "⚡"),
 "docker-na-vps": ("Контейнеры", "Средний", "🐳"),
 "n8n-na-vps": ("Автоматизация", "Средний", "🔗"),
 "wireguard-na-vps": ("Сети", "Средний", "🔒"),
 "minecraft-server-na-vps": ("Игры", "Средний", "⛏️"),
 "uptime-kuma-monitoring-vps": ("Мониторинг", "Средний", "📈"),
 "vaultwarden-na-vps": ("Безопасность", "Средний", "🗝️"),
 "bekapy-vps-restic-rsync": ("Надёжность", "Средний", "💾"),
 "vps-tormozit-diagnostika": ("Диагностика", "Средний", "🩺"),
}
SECTIONS = [
 ("Начните отсюда", "Основы: выбор, подключение, безопасность", ["kak-vybrat-vps","podklyuchenie-k-vps-po-ssh","nastroika-ubuntu-vps","vps-vs-vds-vs-hosting"]),
 ("Практические проекты", "Запускаем боты, сайты, сервисы", ["telegram-bot-na-vps","sajt-na-vps-nginx-ssl","wordpress-na-vps","fastapi-na-vps","docker-na-vps","n8n-na-vps","wireguard-na-vps","minecraft-server-na-vps"]),
 ("Надёжность и обслуживание", "Мониторинг, бэкапы, диагностика, пароли", ["uptime-kuma-monitoring-vps","bekapy-vps-restic-rsync","vps-tormozit-diagnostika","vaultwarden-na-vps"]),
]
order = [s for _,_,l in SECTIONS for s in l]
order.insert(4,"aeza-obzor")
assert set(order)=={a['slug'] for a in ARTS}, set(order)^{a['slug'] for a in ARTS}
bymap = {a['slug']:a for a in ARTS}

CSS = """
:focus-visible{outline:3px solid var(--acc2);outline-offset:4px}.skip{position:absolute;left:12px;top:-80px;z-index:100;background:var(--surface);padding:10px}.skip:focus{top:5px}
.kicker{font:700 .8rem ui-monospace,monospace;letter-spacing:.09em;text-transform:uppercase;color:var(--acc)}.task-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:24px 0}.task-card{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:24px;color:var(--fg);text-decoration:none;display:flex;flex-direction:column;gap:10px}.task-card:hover{border-color:var(--acc)}.task-card b{font-size:1.2rem}.task-card p{font-size:.95rem;color:var(--mut);margin:0}.task-card span{font-size:.9rem;color:var(--acc);margin-top:auto}.tool{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:28px;margin:28px 0}.tool label{display:block;font-weight:600;margin:14px 0 6px}.tool select,.search-input{width:100%;font:inherit;border:1px solid var(--line);background:var(--bg);color:var(--fg);padding:12px;border-radius:10px}.tool output{display:block;padding:20px;background:var(--accsoft);border-radius:12px;margin:20px 0}.tool output b{font-size:1.2rem}.ad-banner{display:block;max-width:640px;margin:32px auto;text-align:center}.ad-banner img{display:block;width:100%;height:auto;border-radius:14px}.ad-banner small{display:block;color:var(--mut);margin-top:5px}.resource-note{font-size:.9rem;color:var(--mut)}.mini-cta{display:flex;align-items:center;justify-content:space-between;gap:16px;background:var(--accsoft);padding:18px;border-radius:12px;margin:24px 0}.mini-cta p{margin:0;font-size:.95rem}.network{display:flex;gap:18px;flex-wrap:wrap;margin:18px 0}.search-input{margin:20px 0 5px}main{min-height:60vh}.privacy-notice{font-size:.85rem;color:var(--mut)}@media(max-width:700px){.task-grid{grid-template-columns:1fr}.task-card{padding:20px}.mini-cta{flex-direction:column;align-items:stretch}.tool{padding:20px}.hero .actions .btn{width:100%;justify-content:center}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}

:root{--bg:#f7f8fb;--surface:#fff;--fg:#14181f;--mut:#5d6776;--line:#e4e8ef;--acc:#4f46e5;--acc2:#0ea5e9;--accsoft:#eef0ff;--codebg:#0d1117;--codefg:#e6edf3;--shadow:0 1px 2px rgba(16,24,40,.05),0 8px 24px rgba(16,24,40,.06);--r:14px}
@media(prefers-color-scheme:dark){:root{--bg:#0b0f16;--surface:#121823;--fg:#e8ecf3;--mut:#9aa6b8;--line:#232c3a;--acc:#8b93ff;--acc2:#38bdf8;--accsoft:#1a2036;--codebg:#070a10;--shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.35)}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:80px}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--acc);text-underline-offset:3px}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
#bar{position:fixed;top:0;left:0;height:3px;width:0;background:linear-gradient(90deg,var(--acc),var(--acc2));z-index:60}
header.top{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;height:60px;gap:12px}
.logo{white-space:nowrap;display:flex;align-items:center;gap:10px;font-weight:800;color:var(--fg);text-decoration:none;letter-spacing:-.01em}
.logo i{width:30px;height:30px;border-radius:9px;background:linear-gradient(135deg,var(--acc),var(--acc2));display:grid;place-items:center;color:#fff;font:700 14px ui-monospace,monospace;font-style:normal}
nav.main{display:flex;align-items:center;gap:6px}nav.main a{color:var(--fg);text-decoration:none;padding:8px 12px;border-radius:9px;font-size:.95rem;font-weight:500}nav.main a:hover{background:var(--accsoft)}
.btn{display:inline-flex;align-items:center;gap:8px;background:linear-gradient(135deg,var(--acc),var(--acc2));color:#fff!important;padding:11px 20px;border-radius:11px;text-decoration:none;font-weight:700;font-size:.97rem;box-shadow:0 6px 18px rgba(79,70,229,.28);transition:transform .15s,box-shadow .15s;border:0}
.btn:hover{transform:translateY(-1px);box-shadow:0 10px 24px rgba(79,70,229,.36)}.btn.ghost{background:var(--surface);color:var(--fg)!important;border:1px solid var(--line);box-shadow:none}.btn.sm{padding:8px 14px;font-size:.9rem;white-space:nowrap}@media(max-width:520px){header.top .wrap{height:56px}.logo{font-size:.95rem}.logo i{width:26px;height:26px}nav.main a{padding:6px 8px;font-size:.9rem}.btn.sm{padding:7px 11px;font-size:.85rem}.hero{padding-top:40px}}
.hero{padding:64px 0 36px;text-align:center;background:radial-gradient(900px 340px at 50% -10%,var(--accsoft),transparent)}
.hero h1{font-size:clamp(2rem,5vw,3.3rem);line-height:1.12;letter-spacing:-.03em;margin:0 auto 16px;max-width:820px}
.hero h1 em{font-style:normal;background:linear-gradient(135deg,var(--acc),var(--acc2));-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p.lead{font-size:1.15rem;color:var(--mut);max-width:640px;margin:0 auto 26px}
.hero .actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.badges{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:26px}
.badge{background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:6px 13px;font-size:.84rem;color:var(--mut)}
.sec{margin:46px 0 10px}.sec h2{font-size:1.55rem;margin:0;letter-spacing:-.02em}.sec p{margin:4px 0 0;color:var(--mut)}
.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));margin:20px 0}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:18px;text-decoration:none;color:var(--fg);display:flex;flex-direction:column;gap:8px;box-shadow:var(--shadow);transition:transform .15s,border-color .15s}
.card:hover{transform:translateY(-3px);border-color:var(--acc)}
.card .ico{width:42px;height:42px;border-radius:12px;background:var(--accsoft);display:grid;place-items:center;font-size:22px}
.card b{font-size:1.04rem;line-height:1.35}.card span.d{color:var(--mut);font-size:.9rem;line-height:1.5;flex:1}
.chips{display:flex;gap:6px;flex-wrap:wrap;align-items:center}.chip{font-size:.74rem;font-weight:700;letter-spacing:.02em;text-transform:uppercase;padding:3px 9px;border-radius:999px;background:var(--accsoft);color:var(--acc)}.chip.lvl{background:transparent;border:1px solid var(--line);color:var(--mut);text-transform:none;font-weight:600}
.promo{margin:46px 0;border-radius:20px;padding:30px;background:linear-gradient(135deg,#312e81,#0369a1);color:#fff;display:flex;gap:24px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.promo h2{margin:0 0 6px;font-size:1.5rem}.promo p{margin:0;opacity:.9;max-width:560px}.promo .btn{background:#fff;color:#312e81!important;box-shadow:none}.promo small{display:block;opacity:.7;margin-top:8px;font-size:.8rem}
.art{display:grid;grid-template-columns:minmax(0,1fr);gap:36px;margin:26px 0 10px}
@media(min-width:980px){.art{grid-template-columns:minmax(0,740px) 300px;justify-content:space-between}}
.crumbs{font-size:.86rem;color:var(--mut);padding-top:20px}.crumbs a{color:var(--mut)}
.arthead h1{font-size:clamp(1.8rem,4vw,2.5rem);line-height:1.2;letter-spacing:-.025em;margin:12px 0}
.arthead .lead{color:var(--mut);font-size:1.08rem;margin:0 0 12px}.meta{color:var(--mut);font-size:.88rem;display:flex;gap:14px;flex-wrap:wrap}
article h2{font-size:1.5rem;line-height:1.3;margin:2.1em 0 .5em;letter-spacing:-.015em}
article p,article li{overflow-wrap:anywhere}article ul,article ol{padding-left:1.3em}article li{margin:.3em 0}
article table{border-collapse:separate;border-spacing:0;width:100%;display:block;overflow-x:auto;margin:1.2em 0;border:1px solid var(--line);border-radius:12px;background:var(--surface)}
td,th{padding:10px 14px;text-align:left;font-size:.93rem;border-bottom:1px solid var(--line);vertical-align:top}th{background:var(--accsoft);font-weight:700}tr:last-child td{border-bottom:0}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.88em}p code,li code,td code{background:var(--accsoft);padding:2px 6px;border-radius:6px;color:var(--acc)}
.pre{position:relative;margin:1.1em 0}.pre pre{margin:0;background:var(--codebg);color:var(--codefg);padding:16px 16px;border-radius:12px;overflow:auto;font-size:.86rem;line-height:1.6;border:1px solid #1f2937}
.pre pre code{background:none;color:inherit;padding:0;font-size:inherit}
.copy{position:absolute;top:8px;right:8px;background:#1f2937;color:#cbd5e1;border:1px solid #334155;border-radius:8px;font:600 12px system-ui;padding:5px 10px;cursor:pointer;opacity:.0;transition:opacity .15s}.pre:hover .copy,.copy:focus{opacity:1}@media(hover:none){.copy{opacity:1}}
.toc{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:16px 18px;box-shadow:var(--shadow)}.toc b{font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--mut)}
.toc ol{list-style:none;margin:10px 0 0;padding:0}.toc li{margin:0}.toc a{display:block;padding:5px 10px;border-left:2px solid var(--line);color:var(--mut);text-decoration:none;font-size:.9rem;line-height:1.4}.toc a.on,.toc a:hover{border-color:var(--acc);color:var(--fg);background:var(--accsoft)}
aside.side{display:none}@media(min-width:980px){aside.side{display:block}.stick{position:sticky;top:84px;display:flex;flex-direction:column;gap:16px}.toc.mob{display:none}}
.toc.mob{margin:18px 0}
.cta{border-radius:16px;padding:20px 22px;margin:2em 0;background:linear-gradient(135deg,var(--accsoft),color-mix(in srgb,var(--acc2) 10%,var(--surface)));border:1px solid color-mix(in srgb,var(--acc) 35%,var(--line))}
.cta strong{font-size:1.08rem;display:block}.cta p{margin:6px 0 12px;color:var(--mut);font-size:.95rem;line-height:1.55}.cta small{display:block;color:var(--mut);margin-top:10px;font-size:.78rem}
.sidecta{border-radius:var(--r);padding:18px;background:linear-gradient(135deg,#312e81,#0369a1);color:#fff}.sidecta b{display:block;font-size:1.05rem;margin-bottom:6px}.sidecta p{margin:0 0 12px;font-size:.88rem;opacity:.9;line-height:1.5}.sidecta .btn{background:#fff;color:#312e81!important;box-shadow:none;width:100%;justify-content:center}.sidecta small{display:block;margin-top:8px;opacity:.7;font-size:.74rem}
details{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:10px 0}summary{cursor:pointer;font-weight:700}details p{margin:.6em 0 0;color:var(--mut)}
.pager{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:34px 0}.pager a{border:1px solid var(--line);background:var(--surface);border-radius:12px;padding:14px 16px;text-decoration:none;color:var(--fg)}.pager a small{display:block;color:var(--mut)}.pager .n{text-align:right}
footer.foot{margin-top:60px;border-top:1px solid var(--line);background:var(--surface);padding:34px 0 40px;color:var(--mut);font-size:.9rem}
footer.foot .cols{display:grid;gap:24px;grid-template-columns:1.4fr 1fr 1fr}@media(max-width:700px){footer.foot .cols{grid-template-columns:1fr}.pager{grid-template-columns:1fr}.pager .n{text-align:left}nav.main a.hide{display:none}}
footer.foot b{color:var(--fg);display:block;margin-bottom:8px}footer.foot a{display:block;color:var(--mut);text-decoration:none;padding:3px 0}footer.foot a:hover{color:var(--acc)}
.simple{max-width:760px;margin:30px auto}
"""

JS = """
(function(){
var bar=document.getElementById('bar');
function p(){var h=document.documentElement;var s=h.scrollTop||document.body.scrollTop;var t=h.scrollHeight-h.clientHeight;if(bar)bar.style.width=(t>0?s/t*100:0)+'%'}
addEventListener('scroll',p,{passive:true});p();
document.querySelectorAll('.pre').forEach(function(w){var b=document.createElement('button');b.className='copy';b.type='button';b.textContent='Копировать';b.onclick=function(){var t=w.querySelector('code').innerText;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){b.textContent='Скопировано ✓';setTimeout(function(){b.textContent='Копировать'},1500)}).catch(function(){var r=document.createRange();r.selectNodeContents(w.querySelector('code'));var s=getSelection();s.removeAllRanges();s.addRange(r)})};w.appendChild(b)});
var links=[].slice.call(document.querySelectorAll('.toc.side a'));
if(links.length&&'IntersectionObserver' in window){var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){links.forEach(function(a){a.classList.remove('on')});var a=map[en.target.id];if(a)a.classList.add('on')}})},{rootMargin:'-80px 0px -70% 0px'});
document.querySelectorAll('article h2[id]').forEach(function(h){io.observe(h)})}
})();
"""

def add_toc(body):
    heads=[]
    def rep(m):
        t=re.sub('<[^>]+>','',m.group(1)); i="s-"+str(len(heads)+1); heads.append((i,t))
        return f'<h2 id="{i}">{m.group(1)}</h2>'
    body=re.sub(r'<h2>(.*?)</h2>',rep,body)
    body=re.sub(r'<pre>(<code>.*?</code>)</pre>',r'<div class="pre"><pre>\1</pre></div>',body,flags=re.S)
    return body,heads

def toc_html(heads,cls):
    return f'<nav class="toc {cls}" aria-label="Содержание"><b>Содержание</b><ol>'+''.join(f'<li><a href="#{i}">{e(t)}</a></li>' for i,t in heads)+'</ol></nav>'

def analytics():
    if not METRICA: return ""
    return f'''<script>window.VPS_METRICA={METRICA};(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a)}})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym({METRICA},"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:false}});</script>'''

def page(title,desc,body,canonical,extra_head="",og_type="website",noindex=False):
    url=SITE+canonical
    robots="noindex" if noindex else "index,follow,max-snippet:-1,max-image-preview:large"
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta name="robots" content="{robots}"><meta name="theme-color" content="#4f46e5">
<meta property="og:type" content="{og_type}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="{NAME}">
{YANDEX}{GOOGLE}<meta name="twitter:card" content="summary"><link rel="alternate" type="application/rss+xml" title="{NAME}" href="{SITE}/rss.xml">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%234f46e5'/%3E%3Ctext x='32' y='43' font-size='30' text-anchor='middle' fill='white' font-family='monospace'%3E%3E_%3C/text%3E%3C/svg%3E">
<style>{CSS}</style>{extra_head}{analytics()}</head><body><a class="skip" href="#main">К содержанию</a><div id="bar"></div>
<header class="top"><div class="wrap"><a class="logo" href="/"><i>&gt;_</i>{NAME}</a><nav class="main"><a href="/articles/">Статьи</a><a class="hide" href="/about/">О сайте</a><a class="btn sm" href="{REF}" rel="sponsored nofollow noopener" target="_blank">Тарифы Aeza</a></nav></div></header>
<main id="main">{body}</main>
<footer class="foot"><div class="wrap"><div class="cols"><div><b>{NAME}</b><p>{e(TAG)}. Примеры для Ubuntu 22.04 и 24.04; проверяйте совместимость с вашим окружением.</p><p>Раскрытие: на сайте есть партнёрские ссылки на хостинг Aeza. Автор может получить вознаграждение. <a style="display:inline" href="/about/">Подробнее</a></p></div>
<div><b>Рубрики</b><a href="/articles/">Все статьи</a><a href="/articles/kak-vybrat-vps/">Выбор VPS</a><a href="/articles/nastroika-ubuntu-vps/">Безопасность</a><a href="/articles/docker-na-vps/">Docker</a></div>
<div><b>Сайт</b><a href="/about/">О сайте</a><a href="/rss.xml">RSS</a><a href="/sitemap.xml">Карта сайта</a><a href="/privacy/">Конфиденциальность</a><span>© {datetime.date.today().year}</span></div></div></div></footer>
<script>{JS}</script><script src="/assets/growth.js" defer></script></body></html>'''

def w(path,content):
    p=os.path.join(OUT,path.lstrip('/'));os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,'w',encoding='utf-8').write(content)
def jld(o): return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>'
def mins(a): return max(2,round(len(re.sub('<[^>]+>',' ',a['body']).split())/180))
def card(a):
    c,l,i=META[a['slug']]
    return f'<a class="card" href="/articles/{a["slug"]}/"><div class="ico">{i}</div><div class="chips"><span class="chip">{c}</span><span class="chip lvl">{l}</span></div><b>{e(a["h1"])}</b><span class="d">{e(a["desc"][:130].rsplit(" ",1)[0])}…</span><span class="meta">~{mins(a)} мин чтения</span></a>'

shutil.rmtree(OUT,ignore_errors=True)
shutil.copytree("assets",os.path.join(OUT,"assets"),dirs_exist_ok=True)

for n,a in enumerate(ARTS):
    body,heads=add_toc(a['body'])
    topic=a['slug']
    if topic=='telegram-bot-na-vps': body+=f'<p>Нужен готовый файл автозапуска? <a href="{BOT_SITE}systemd/">Соберите unit systemd для своего бота</a>.</p>'
    if topic=='n8n-na-vps': body+=f'<p>Для отдельного проекта: <a href="{FLOW_SITE}compose/">генератор Docker Compose с HTTPS и PostgreSQL</a>.</p>'
    intent='бота' if 'bot' in topic else 'n8n' if 'n8n' in topic else 'проекта'
    top_cta=f'<div class="mini-cta"><p><b>Сначала — ресурсы под задачу.</b><br>Оцените конфигурацию для {intent}, затем сравните тарифы.</p><a class="btn ghost" href="/choose/">Подобрать конфигурацию →</a></div>' 
    c,l,ic=META[a['slug']]
    i=order.index(a['slug']); prv=bymap[order[i-1]] if i>0 else None; nxt=bymap[order[i+1]] if i<len(order)-1 else None
    rel=[bymap[order[(i+k)%len(order)]] for k in (1,2,3)]
    faq=''.join(f'<details><summary>{e(q)}</summary><p>{e(an)}</p></details>' for q,an in a['faq'])
    url=f"{SITE}/articles/{a['slug']}/"
    ld=[
     {"@context":"https://schema.org","@type":"Article","headline":a['h1'],"description":a['desc'],"inLanguage":"ru","datePublished":a['date'],"dateModified":a.get("modified",a["date"]),"mainEntityOfPage":url,"articleSection":c,"author":{"@type":"Organization","name":NAME,"url":SITE},"publisher":{"@type":"Organization","name":NAME,"url":SITE},"keywords":a['kw']},
     {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":an}} for q,an in a['faq']]},
     {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Главная","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Статьи","item":SITE+"/articles/"},{"@type":"ListItem","position":3,"name":a['h1'],"item":url}]}]
    pager='<div class="pager">'+(f'<a href="/articles/{prv["slug"]}/"><small>← Предыдущая</small>{e(prv["h1"])}</a>' if prv else '<span></span>')+(f'<a class="n" href="/articles/{nxt["slug"]}/"><small>Следующая →</small>{e(nxt["h1"])}</a>' if nxt else '<span></span>')+'</div>'
    side=f'''<aside class="side"><div class="stick">{toc_html(heads,"side")}<div class="sidecta"><b>Нужен сервер?</b><p>Все команды из статьи подойдут для любого VPS на Ubuntu. Тарифы и локации — на сайте Aeza.</p><a class="btn" href="{REF}" rel="sponsored nofollow noopener" target="_blank">Смотреть тарифы →</a><small>Партнёрская ссылка</small></div></div></aside>'''
    html_body=f'''<div class="wrap"><div class="crumbs"><a href="/">Главная</a> › <a href="/articles/">Статьи</a> › {c}</div>
<div class="art"><div><div class="arthead"><div class="chips"><span class="chip">{c}</span><span class="chip lvl">{l}</span></div><h1>{e(a['h1'])}</h1><p class="lead">{e(a['desc'])}</p><div class="meta"><span>Редакция: {a.get("modified",a["date"])}</span><span>~{mins(a)} мин чтения</span><span>Ubuntu 22.04 / 24.04</span></div></div>
{top_cta}{toc_html(heads,"mob")}<article>{body}<h2>Частые вопросы</h2>{faq}</article>{pager}
<div class="sec"><h2>Читайте также</h2></div><div class="grid">{''.join(card(x) for x in rel)}</div></div>{side}</div></div>'''
    w(f"articles/{a['slug']}/index.html",page(a['title'],a['desc'],html_body,f"/articles/{a['slug']}/",''.join(jld(x) for x in ld),"article"))

secs=''.join(f'<div class="sec"><h2>{t}</h2><p>{s}</p></div><div class="grid">{"".join(card(bymap[x]) for x in l)}</div>' for t,s,l in SECTIONS)
home=f'''<section class="hero"><div class="wrap"><h1>VPS без боли: <em>пошаговые инструкции</em> с рабочими командами</h1>
<p class="lead">Как выбрать сервер, защитить его и запустить на нём бота, сайт, WireGuard или n8n. Выберите ресурсы под задачу, пройдите инструкцию и настройте резервные копии.</p>
<div class="actions"><a class="btn" href="/articles/kak-vybrat-vps/">Начать с выбора VPS →</a><a class="btn ghost" href="/articles/">Все {len(ARTS)} статей</a></div>
<div class="badges"><span class="badge">Ubuntu 22.04 / 24.04</span><span class="badge">✓ Команды копируются одной кнопкой</span><span class="badge">✓ Для новичков и практиков</span></div></div></section>
<div class="wrap">{secs}
<div class="promo"><div><h2>Нужен сервер для практики?</h2><p>Все инструкции подходят для любого VPS на Ubuntu. Сравните подходящие конфигурации и доступные локации Aeza перед заказом.</p><small>Партнёрская ссылка: цена для вас не меняется. <a style="color:#fff" href="/articles/aeza-obzor/">Читать обзор Aeza</a></small></div><a class="btn" href="{REF}" rel="sponsored nofollow noopener" target="_blank">Тарифы Aeza →</a></div></div>'''
tasks=f'''<section class="wrap"><div class="sec"><span class="kicker">От задачи к работающему серверу</span><h2>Что хотите запустить?</h2></div><div class="task-grid"><a class="task-card" href="{BOT_SITE}"><b>Telegram-бот</b><p>Оценка ресурсов, автозапуск и разбор ошибок. Бот продолжает работать после закрытия ноутбука.</p><span>Собрать план запуска →</span></a><a class="task-card" href="{FLOW_SITE}"><b>Автоматизации n8n</b><p>Конфигурация с HTTPS и базой данных, резервные копии и контроль расходов на API.</p><span>Подготовить n8n →</span></a><a class="task-card" href="/choose/"><b>Сайт или другой проект</b><p>Подберите стартовую конфигурацию без обещаний универсального тарифа для всех.</p><span>Оценить ресурсы →</span></a></div></section>'''
home=home.replace('<div class="wrap">'+secs,tasks+'<div class="wrap">'+secs)
home+=f'<div class="wrap"><a class="ad-banner" href="{REF}" data-placement="home-banner" target="_blank" rel="sponsored nofollow noopener"><img src="/assets/aeza-cloud.webp" width="960" height="540" alt="Облачный сервер Aeza — посмотреть условия" loading="lazy"><small>Реклама · партнёрская ссылка · условия у провайдера</small></a></div>'
w("index.html",page(f"{NAME} — инструкции по VPS: настройка, боты, сайты, WireGuard","Пошаговые инструкции по VPS на Ubuntu: как выбрать сервер, защитить его, запустить Telegram-бота, сайт на Nginx, WireGuard, Docker, n8n и Minecraft.",home,"/",jld({"@context":"https://schema.org","@type":"WebSite","name":NAME,"url":SITE+"/","inLanguage":"ru"})))
w("articles/index.html",page(f"Все статьи — {NAME}","Каталог инструкций по VPS: выбор, настройка, безопасность, боты, сайты, VPN, Docker, мониторинг и бэкапы.",f'<div class="wrap"><div class="crumbs"><a href="/">Главная</a> › Статьи</div><h1>Инструкции по VPS: от выбора до эксплуатации</h1>{secs}<div class="sec"><h2>Обзор хостинга</h2></div><div class="grid">{card(bymap["aeza-obzor"])}</div></div>',"/articles/"))
about=f'''<div class="wrap"><div class="simple"><h1>О сайте и раскрытие партнёрских отношений</h1>
<p>{NAME} — независимый справочник практических инструкций по администрированию VPS. Все команды проверяйте на тестовом сервере перед использованием в работе.</p>
<h2>Партнёрские ссылки</h2><p>Часть ссылок на хостинг Aeza содержит реферальный код. Если вы зарегистрируетесь по такой ссылке и закажете услугу, автор сайта может получить вознаграждение. Для вас цена не меняется. Партнёрские ссылки помечены атрибутами <code>rel="sponsored nofollow"</code>.</p>
<h2>Ограничения</h2><p>Тарифы, цены и характеристики хостеров меняются. Актуальную информацию всегда сверяйте на официальном сайте поставщика. Материалы носят информационный характер.</p>
<h2>Реклама</h2><p>Сайт содержит рекламу партнёрской программы хостинга Aeza.</p></div></div>'''
w("about/index.html",page(f"О сайте — {NAME}","О проекте, раскрытие партнёрских ссылок и ограничения ответственности.",about,"/about/"))
w("404.html",page(f"Страница не найдена — {NAME}","Страница не найдена.","<div class='wrap'><div class='simple'><h1>404 — страница не найдена</h1><p><a href='/'>На главную</a> или <a href='/articles/'>к статьям</a>.</p></div></div>","/404.html",noindex=True))

choose='''<div class="wrap"><section class="hero"><span class="kicker">Подбор VPS</span><h1>Начните с задачи,<br>а не с самого дорогого тарифа</h1><p class="lead">Ориентировочная конфигурация для старта. Реальные требования зависят от приложения и нагрузки.</p></section><form class="tool" id="vps-picker"><label for="task">Что запускаете?</label><select id="task" name="task"><option value="bot">Telegram-бот</option><option value="n8n">n8n и автоматизации</option><option value="site">Небольшой сайт</option><option value="minecraft">Minecraft Java</option></select><label for="load">Нагрузка</label><select id="load" name="load"><option value="small">Небольшой личный проект</option><option value="medium">База данных и несколько процессов</option><option value="large">Тяжёлые задачи / моды / обработка файлов</option></select><output id="picker-result" aria-live="polite"><b>1 vCPU · 1–2 ГБ RAM · 20 ГБ SSD</b><p>Стартовый ориентир для небольшого бота. Следите за памятью процесса.</p></output><a class="btn" href="https://aeza.ru/?ref=467715" data-placement="picker-result" rel="sponsored nofollow noopener" target="_blank">Сравнить подходящие тарифы Aeza →</a><p class="privacy-notice">Реклама · партнёрская ссылка. Наличие конфигураций и цены проверяйте у провайдера.</p></form><h2>Что проверить перед оплатой</h2><ol><li>Стоимость месяца и условия продления, а не только стартовую скидку.</li><li>Доступность нужной локации и сервисов из неё.</li><li>Входят ли резервные копии; храните отдельную копию вне этого VPS.</li><li>Можно ли увеличить RAM и диск без сложного переноса.</li></ol><p><a href="/articles/kak-vybrat-vps/">Подробный чек-лист выбора VPS →</a></p></div>'''
w("choose/index.html",page("Подбор VPS под бота, n8n, сайт или Minecraft", "Подберите ориентировочную конфигурацию VPS по задаче и нагрузке: CPU, RAM, диск и важные проверки перед заказом.",choose,"/choose/"))
privacy='''<div class="wrap"><div class="simple"><h1>Конфиденциальность</h1><p>На сайте используется Яндекс Метрика для анализа посещений и действий: открытия страниц, подбора конфигурации, скачивания примеров и переходов по партнёрским ссылкам. Запись сессий Вебвизором отключена. Метрика может использовать cookie и обрабатывать технические сведения о браузере, устройстве и посещении.</p><p>Не вводите токены, пароли и личные сведения в инструменты сайта. Подбор ресурсов выполняется в браузере; значения секретов для него не нужны. На сайте нет регистрации и форм отправки заявок.</p><p>Переход в Aeza открывает сторонний сайт с его условиями обработки данных. Автор не получает доступ к вашему аккаунту или платежным данным. Регистрации и оплаты не измеряются как подтверждённые конверсии на этом сайте: доступен только учёт переходов.</p><p>Подробности: <a href="https://yandex.ru/legal/confidential/">политика Яндекса</a>, <a href="https://aeza.ru/privacy">политика Aeza</a>.</p></div></div>'''
w("privacy/index.html",page("Конфиденциальность — VPS на практике","Информация об аналитике, партнёрских ссылках и работе инструментов сайта.",privacy,"/privacy/"))
urls=[("/",TODAY,"1.0"),("/articles/",TODAY,"0.8"),("/about/",TODAY,"0.3"),("/choose/",TODAY,"0.8"),("/privacy/",TODAY,"0.2")]+[(f"/articles/{a['slug']}/",a.get("modified",a["date"]),"0.9") for a in ARTS]
w("sitemap.xml",'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod><priority>{p}</priority></url>' for u,d,p in urls)+'</urlset>')
w("robots.txt",f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
w("rss.xml",'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>'+NAME+'</title><link>'+SITE+'/</link><description>'+e(TAG)+'</description><language>ru</language>'+''.join(f'<item><title>{e(a["h1"])}</title><link>{SITE}/articles/{a["slug"]}/</link><guid>{SITE}/articles/{a["slug"]}/</guid><description>{e(a["desc"])}</description></item>' for a in ARTS)+'</channel></rss>')
w(f"{KEY}.txt",KEY)
open(os.path.join(OUT,"CNAME"),"w").write(SITE.split("//")[1])
open(os.path.join(OUT,".nojekyll"),"w").close()
open("indexnow.json","w").write(json.dumps({"host":SITE.split('//')[1],"key":KEY,"keyLocation":f"{SITE}/{KEY}.txt","urlList":[SITE+u for u,_,_ in urls]},ensure_ascii=False))
print("built",len(ARTS),"articles")
