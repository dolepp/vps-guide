from articles1 import cta, REF
B = []

B.append(dict(
slug="telegram-bot-na-vps",
title="Как запустить Telegram-бота на VPS 24/7: Python, venv и systemd",
h1="Telegram-бот на VPS: запуск 24/7 через systemd",
desc="Пошаговая инструкция: как перенести Telegram-бота на Python на VPS, настроить виртуальное окружение, автозапуск через systemd и просмотр логов.",
kw="telegram бот на vps, запуск бота 24/7, systemd python бот, хостинг для телеграм бота",
date="2026-11-05",
body=f'''
<p>Бот на домашнем компьютере работает, пока включён компьютер. Чтобы он отвечал круглосуточно, его переносят на VPS. Для большинства ботов хватает минимального тарифа: 1 ядро и 512 МБ – 1 ГБ RAM. Ниже полный путь на примере Python и библиотеки aiogram (подходит и для python-telegram-bot, и для Telethon).</p>

<h2>Что понадобится</h2>
<ul><li>VPS с Ubuntu 22.04/24.04 (<a href="/articles/kak-vybrat-vps/">как выбрать</a>);</li>
<li>токен бота от @BotFather;</li>
<li>код бота в папке или Git-репозитории.</li></ul>
<p>Перед запуском сделайте <a href="/articles/nastroika-ubuntu-vps/">базовую настройку безопасности сервера</a>.</p>

<h2>1. Установите Python и зависимости</h2>
<pre><code>sudo apt update
sudo apt install -y python3 python3-venv python3-pip git</code></pre>

<h2>2. Загрузите проект</h2>
<pre><code>cd ~
git clone https://github.com/ВАШ_ЛОГИН/ВАШ_БОТ.git bot
cd bot</code></pre>
<p>Без Git можно скопировать файлы командой <code>scp -r ./bot deploy@IP:~/</code> со своего компьютера.</p>

<h2>3. Виртуальное окружение</h2>
<pre><code>python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt</code></pre>

<h2>4. Храните токен в переменных окружения</h2>
<p>Не кладите токен в код. Создайте файл <code>.env</code> и закройте права:</p>
<pre><code>echo 'BOT_TOKEN=123456:ABC...' &gt; .env
chmod 600 .env</code></pre>

<h2>5. Автозапуск через systemd</h2>
<pre><code>sudo nano /etc/systemd/system/mybot.service</code></pre>
<pre><code>[Unit]
Description=My Telegram Bot
After=network-online.target
Wants=network-online.target

[Service]
User=deploy
WorkingDirectory=/home/deploy/bot
EnvironmentFile=/home/deploy/bot/.env
ExecStart=/home/deploy/bot/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target</code></pre>
<pre><code>sudo systemctl daemon-reload
sudo systemctl enable --now mybot
sudo systemctl status mybot</code></pre>
<p><code>Restart=always</code> перезапустит бота при падении, а <code>enable</code> — после перезагрузки сервера.</p>

<h2>6. Логи</h2>
<pre><code>journalctl -u mybot -f          # живой поток
journalctl -u mybot --since "1 hour ago"</code></pre>

<h2>7. Обновление бота</h2>
<pre><code>cd ~/bot &amp;&amp; git pull
source venv/bin/activate &amp;&amp; pip install -r requirements.txt
sudo systemctl restart mybot</code></pre>

{cta("Бот готов, осталось где его запустить")}

<h2>Частые проблемы</h2>
<ul>
<li><b>Бот не стартует:</b> смотрите <code>journalctl -u mybot -n 50</code> — чаще всего не хватает зависимости или переменной окружения.</li>
<li><b>Ошибка «Conflict: terminated by other getUpdates»:</b> бот уже запущен в другом месте (на домашнем ПК). Остановите копию.</li>
<li><b>Бот падает от нехватки памяти:</b> добавьте swap или возьмите тариф побольше.</li>
<li><b>Нужна база данных:</b> для простых задач хватит SQLite, для нагрузки — PostgreSQL.</li>
</ul>
''',
faq=[
("Сколько стоит содержать Telegram-бота на VPS?","Для небольшого бота подходит самый дешёвый тариф VPS. Точную цену смотрите у выбранного хостера."),
("Можно ли запускать несколько ботов на одном VPS?","Да. Делайте для каждого отдельный systemd-сервис и виртуальное окружение. Ресурсов 1 ГБ RAM хватит на несколько лёгких ботов."),
("Как сделать, чтобы бот не падал?","Параметр Restart=always в systemd перезапускает процесс автоматически, а логи через journalctl помогают найти причину сбоев."),
]))

B.append(dict(
slug="sajt-na-vps-nginx-ssl",
title="Как разместить сайт на VPS: Nginx, домен и бесплатный SSL Let's Encrypt",
h1="Сайт на VPS: Nginx + HTTPS за 20 минут",
desc="Инструкция по размещению сайта на VPS с Ubuntu: установка Nginx, настройка домена и DNS, бесплатный SSL-сертификат Let's Encrypt и автопродление.",
kw="сайт на vps, nginx ubuntu настройка, ssl let's encrypt certbot, разместить сайт на vps",
date="2026-11-05",
body=f'''
<p>Собственный VPS даёт полный контроль над сайтом: вы выбираете стек, не зависите от ограничений тарифа и платите за ресурсы. Разберём самый универсальный вариант: Nginx раздаёт статические файлы (или проксирует на ваше приложение) и работает по HTTPS.</p>

<h2>Что нужно</h2>
<ul><li>VPS на Ubuntu с <a href="/articles/nastroika-ubuntu-vps/">базовой защитой</a>;</li><li>домен и доступ к его DNS;</li><li>файлы сайта.</li></ul>

<h2>1. Направьте домен на сервер</h2>
<p>В DNS-панели регистратора создайте A-записи для <code>example.com</code> и <code>www.example.com</code> на IP сервера (для IPv6 — AAAA). Обновление обычно занимает от нескольких минут до пары часов. Проверка:</p>
<pre><code>dig +short example.com</code></pre>

<h2>2. Установите Nginx</h2>
<pre><code>sudo apt update
sudo apt install -y nginx
sudo ufw allow 'Nginx Full'
sudo systemctl enable --now nginx</code></pre>

<h2>3. Конфигурация сайта</h2>
<pre><code>sudo mkdir -p /var/www/example.com
sudo chown -R $USER:$USER /var/www/example.com
echo '&lt;h1&gt;Привет, VPS!&lt;/h1&gt;' &gt; /var/www/example.com/index.html
sudo nano /etc/nginx/sites-available/example.com</code></pre>
<pre><code>server {{
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    root /var/www/example.com;
    index index.html;

    location / {{
        try_files $uri $uri/ =404;
    }}
}}</code></pre>
<pre><code>sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
sudo nginx -t &amp;&amp; sudo systemctl reload nginx</code></pre>

<h2>4. Бесплатный SSL (Let's Encrypt)</h2>
<pre><code>sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com</code></pre>
<p>Certbot сам добавит HTTPS в конфиг и настроит редирект с HTTP. Автопродление проверьте командой:</p>
<pre><code>sudo certbot renew --dry-run</code></pre>

{cta("Сайту нужен свой сервер?")}

<h2>5. Если у вас приложение (Node, Python), а не статика</h2>
<p>Nginx работает как обратный прокси:</p>
<pre><code>location / {{
    proxy_pass http://127.0.0.1:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-Proto $scheme;
}}</code></pre>
<p>Само приложение запускайте через systemd так же, как <a href="/articles/telegram-bot-na-vps/">бота</a>.</p>

<h2>6. Ускорение и безопасность</h2>
<ul>
<li>включите gzip или brotli, кэширование статики (<code>expires 30d</code>);</li>
<li>скройте версию Nginx: <code>server_tokens off;</code>;</li>
<li>настройте бэкап каталога сайта и базы данных.</li>
</ul>
''',
faq=[
("Нужно ли покупать SSL-сертификат?","Нет, для большинства сайтов хватает бесплатных сертификатов Let's Encrypt с автопродлением."),
("Сколько ресурсов нужно для небольшого сайта?","Для статики или лёгкого блога достаточно 1 ядра и 1 ГБ RAM, WordPress с базой комфортнее на 2 ГБ."),
("Что лучше: Nginx или Apache?","Nginx экономнее по памяти и хорош как веб-сервер и обратный прокси. Apache удобен, если нужны .htaccess-файлы."),
]))

B.append(dict(
slug="wireguard-na-vps",
title="Свой WireGuard на VPS: настройка личного сервера для защиты трафика",
h1="WireGuard на VPS: личный защищённый туннель",
desc="Пошаговая настройка WireGuard на Ubuntu VPS: ключи, wg0.conf, NAT, UFW и конфиг клиента. Для безопасной работы в публичных сетях.",
kw="wireguard на vps, настройка wireguard ubuntu, свой vpn сервер, личный впн на vps",
date="2026-11-05",
body=f'''
<p>WireGuard — быстрый и простой VPN-протокол, встроенный в ядро Linux. Личный сервер полезен, чтобы безопасно работать в публичном Wi-Fi, получать доступ к домашней сети или рабочим ресурсам и шифровать трафик между своими устройствами. Используйте его в соответствии с законодательством вашей страны и правилами хостера.</p>

<h2>Требования</h2>
<p>Подойдёт самый скромный VPS: 1 ядро и 512 МБ RAM. Нужна KVM-виртуализация и Ubuntu 22.04/24.04. Предварительно выполните <a href="/articles/nastroika-ubuntu-vps/">базовую настройку</a>.</p>

<h2>1. Установка</h2>
<pre><code>sudo apt update
sudo apt install -y wireguard</code></pre>

<h2>2. Ключи сервера и клиента</h2>
<pre><code>cd /etc/wireguard
umask 077
wg genkey | tee server.key | wg pubkey &gt; server.pub
wg genkey | tee client.key | wg pubkey &gt; client.pub</code></pre>

<h2>3. Включите маршрутизацию</h2>
<pre><code>echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-wg.conf
sudo sysctl --system</code></pre>

<h2>4. Конфиг сервера</h2>
<p>Узнайте имя внешнего интерфейса командой <code>ip route | grep default</code> (часто <code>eth0</code> или <code>ens3</code>) и подставьте вместо <code>eth0</code>.</p>
<pre><code>sudo nano /etc/wireguard/wg0.conf</code></pre>
<pre><code>[Interface]
Address = 10.8.0.1/24
ListenPort = 51820
PrivateKey = СОДЕРЖИМОЕ_server.key
PostUp = iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE

[Peer]
PublicKey = СОДЕРЖИМОЕ_client.pub
AllowedIPs = 10.8.0.2/32</code></pre>

<h2>5. Файрвол и запуск</h2>
<pre><code>sudo ufw allow 51820/udp
sudo ufw route allow in on wg0 out on eth0
sudo systemctl enable --now wg-quick@wg0
sudo wg show</code></pre>

<h2>6. Конфиг клиента</h2>
<pre><code>[Interface]
PrivateKey = СОДЕРЖИМОЕ_client.key
Address = 10.8.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = СОДЕРЖИМОЕ_server.pub
Endpoint = IP_СЕРВЕРА:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25</code></pre>
<p>Импортируйте файл в приложение WireGuard (Windows, macOS, Linux, Android, iOS). Для телефона удобно сгенерировать QR-код: <code>sudo apt install qrencode &amp;&amp; qrencode -t ansiutf8 &lt; client.conf</code>.</p>

{cta("Для личного VPN подойдёт даже минимальный тариф")}

<h2>Проверка</h2>
<ul>
<li>после подключения ваш внешний IP должен стать IP сервера;</li>
<li><code>sudo wg show</code> покажет последний handshake и объём трафика;</li>
<li>если интернета нет — проверьте имя интерфейса в <code>PostUp</code> и разрешённый UDP-порт.</li>
</ul>

<h2>Добавить ещё одно устройство</h2>
<p>Сгенерируйте новую пару ключей и добавьте в <code>wg0.conf</code> ещё один блок <code>[Peer]</code> с адресом <code>10.8.0.3/32</code>, затем выполните <code>sudo systemctl restart wg-quick@wg0</code>.</p>
''',
faq=[
("WireGuard или OpenVPN — что выбрать?","WireGuard проще в настройке, быстрее и экономнее по ресурсам. OpenVPN нужен в случаях, когда требуется TCP или специфичная совместимость."),
("Сколько устройств выдержит минимальный VPS?","Десятки устройств с лёгким трафиком. Ограничивает чаще пропускная способность канала, а не процессор."),
("Почему не работает интернет через VPN?","Чаще всего неверно указан внешний интерфейс в PostUp, не включён ip_forward или закрыт UDP-порт."),
]))
