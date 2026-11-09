from articles1 import cta, REF
D = []

D.append(dict(
slug="podklyuchenie-k-vps-po-ssh",
title="Как подключиться к VPS по SSH: Windows, macOS, Linux, PuTTY и ключи",
h1="Подключение к VPS по SSH: пошагово для Windows, macOS и Linux",
desc="Как подключиться к VPS по SSH с Windows 10/11, macOS и Linux: команда ssh, PuTTY, SSH-ключи, файл config, копирование файлов через scp и разбор частых ошибок.",
kw="как подключиться к vps, ssh подключение windows, putty vps, ssh ключ, permission denied publickey",
date="2026-11-05",
body=f'''
<p>После заказа VPS хостер присылает IP-адрес, логин (обычно <code>root</code>) и пароль или просит загрузить SSH-ключ. Подключаются к серверу по протоколу SSH. Это одна команда, и работает она в любой современной ОС без установки дополнительных программ.</p>

<h2>Подключение с Windows 10 и 11</h2>
<p>В Windows уже встроен OpenSSH. Откройте PowerShell или «Терминал» и выполните:</p>
<pre><code>ssh root@IP_СЕРВЕРА</code></pre>
<p>При первом подключении система спросит, доверять ли серверу. Введите <code>yes</code>, затем пароль. При вводе пароля символы не отображаются — это нормально.</p>
<p>Если предпочитаете графическую программу, используйте PuTTY: в поле Host Name впишите IP, порт 22, тип Connection type — SSH, нажмите Open.</p>

<h2>Подключение с macOS и Linux</h2>
<p>Откройте Терминал и выполните ту же команду: <code>ssh root@IP_СЕРВЕРА</code>.</p>

<h2>Вход по SSH-ключу вместо пароля</h2>
<p>Ключ надёжнее пароля: его нельзя подобрать. На своём компьютере:</p>
<pre><code>ssh-keygen -t ed25519 -C "my-laptop"
ssh-copy-id root@IP_СЕРВЕРА</code></pre>
<p>В Windows нет <code>ssh-copy-id</code>. Выведите публичный ключ командой <code>type $env:USERPROFILE\\.ssh\\id_ed25519.pub</code> и добавьте строку на сервер в файл <code>~/.ssh/authorized_keys</code>. Затем <a href="/articles/nastroika-ubuntu-vps/">отключите вход по паролю</a>.</p>

<h2>Короткое имя вместо IP</h2>
<p>Создайте файл <code>~/.ssh/config</code> (в Windows: <code>C:\\Users\\ИМЯ\\.ssh\\config</code>):</p>
<pre><code>Host myvps
    HostName IP_СЕРВЕРА
    User deploy
    Port 22
    IdentityFile ~/.ssh/id_ed25519</code></pre>
<p>Теперь подключение: <code>ssh myvps</code>.</p>

{cta("Заказали сервер и ждёте доступы?")}

<h2>Копирование файлов</h2>
<pre><code>scp ./file.zip myvps:/home/deploy/        # на сервер
scp myvps:/home/deploy/file.zip ./        # с сервера
scp -r ./project myvps:/home/deploy/      # папка</code></pre>
<p>Для больших каталогов удобнее <code>rsync -avz ./project/ myvps:/home/deploy/project/</code>: он копирует только изменения.</p>

<h2>Частые ошибки</h2>
<ul>
<li><b>Connection timed out</b> — неверный IP, сервер выключен или порт 22 закрыт файрволом. Проверьте статус в панели хостера.</li>
<li><b>Connection refused</b> — SSH-служба не запущена или слушает другой порт.</li>
<li><b>Permission denied (publickey)</b> — сервер принимает только ключи, а ваш ключ не загружен. Проверьте <code>authorized_keys</code> и права: каталог <code>.ssh</code> — 700, файл ключей — 600.</li>
<li><b>REMOTE HOST IDENTIFICATION HAS CHANGED</b> — вы переустановили сервер, и отпечаток изменился. Удалите старую запись: <code>ssh-keygen -R IP_СЕРВЕРА</code>.</li>
<li><b>Соединение обрывается через минуту простоя</b> — добавьте в config <code>ServerAliveInterval 30</code>.</li>
</ul>
<p>Следующий шаг — <a href="/articles/nastroika-ubuntu-vps/">первичная настройка безопасности</a>.</p>
''',
faq=[
("Какой логин у нового VPS?","Чаще всего root, но у некоторых образов Ubuntu это ubuntu или debian. Точный логин указан в письме хостера или в панели."),
("Можно ли подключиться к VPS с телефона?","Да, подойдут приложения Termius, JuiceSSH или Termux. Лучше использовать вход по ключу."),
("Что лучше: PuTTY или встроенный ssh?","Встроенный OpenSSH проще: одна команда, поддержка config и scp. PuTTY нужен тем, кому удобнее графический интерфейс."),
]))

D.append(dict(
slug="wordpress-na-vps",
title="WordPress на VPS: установка на Nginx, PHP-FPM и MariaDB с SSL",
h1="WordPress на VPS: полная установка на Nginx",
desc="Как установить WordPress на VPS с Ubuntu: Nginx, PHP-FPM, MariaDB, создание базы, настройка конфига, права на файлы и бесплатный SSL Let's Encrypt.",
kw="wordpress на vps, установка wordpress nginx, lemp ubuntu, wordpress ubuntu 24.04",
date="2026-11-05",
body=f'''
<p>WordPress на собственном VPS работает быстрее, чем на дешёвом общем хостинге, и не ограничивает плагины. Стек называется LEMP: Linux, Nginx, MariaDB, PHP. Подойдёт сервер от 1–2 ГБ RAM и 2 ядер; перед началом выполните <a href="/articles/nastroika-ubuntu-vps/">базовую настройку сервера</a> и направьте домен на IP.</p>

<h2>1. Установите пакеты</h2>
<pre><code>sudo apt update
sudo apt install -y nginx mariadb-server php-fpm php-mysql php-curl php-gd php-mbstring php-xml php-zip php-intl unzip curl</code></pre>

<h2>2. Защитите MariaDB и создайте базу</h2>
<pre><code>sudo mysql_secure_installation
sudo mysql</code></pre>
<pre><code>CREATE DATABASE wp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'wpuser'@'localhost' IDENTIFIED BY 'СЛОЖНЫЙ_ПАРОЛЬ';
GRANT ALL PRIVILEGES ON wp.* TO 'wpuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;</code></pre>

<h2>3. Скачайте WordPress</h2>
<pre><code>cd /tmp
curl -LO https://wordpress.org/latest.tar.gz
tar xzf latest.tar.gz
sudo mkdir -p /var/www/example.com
sudo cp -a wordpress/. /var/www/example.com/
sudo chown -R www-data:www-data /var/www/example.com
cd /var/www/example.com
sudo -u www-data cp wp-config-sample.php wp-config.php
sudo -u www-data nano wp-config.php</code></pre>
<p>Впишите <code>DB_NAME</code> = wp, <code>DB_USER</code> = wpuser и пароль. Уникальные ключи безопасности возьмите на <code>api.wordpress.org/secret-key/1.1/salt/</code> и замените блок в файле.</p>

<h2>4. Конфиг Nginx</h2>
<p>Версию сокета PHP-FPM посмотрите командой <code>ls /run/php/</code> (например, <code>php8.3-fpm.sock</code>).</p>
<pre><code>sudo nano /etc/nginx/sites-available/example.com</code></pre>
<pre><code>server {{
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    root /var/www/example.com;
    index index.php index.html;
    client_max_body_size 64M;

    location / {{
        try_files $uri $uri/ /index.php?$args;
    }}
    location ~ \\.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.3-fpm.sock;
    }}
    location ~ /\\.ht {{ deny all; }}
}}</code></pre>
<pre><code>sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
sudo nginx -t &amp;&amp; sudo systemctl reload nginx</code></pre>

<h2>5. SSL</h2>
<pre><code>sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com</code></pre>
<p>Откройте <code>https://example.com</code> и завершите установку в браузере.</p>

{cta("WordPress приятнее на быстром диске и 2+ ГБ памяти")}

<h2>6. Что настроить после установки</h2>
<ul>
<li>В <code>/etc/php/*/fpm/php.ini</code> увеличьте <code>upload_max_filesize</code> и <code>post_max_size</code> до 64M.</li>
<li>Установите плагин кэширования (например, WP Super Cache или LiteSpeed Cache в режиме без LiteSpeed).</li>
<li>Включите автообновления безопасности WordPress и настройте <a href="/articles/bekapy-vps-restic-rsync/">бэкапы</a> базы и каталога <code>wp-content</code>.</li>
<li>Закройте <code>xmlrpc.php</code>, если он вам не нужен.</li>
</ul>
''',
faq=[
("Сколько RAM нужно для WordPress?","Для небольшого блога хватит 1 ГБ с кэшированием. Для магазина или сайта с трафиком берите 2–4 ГБ."),
("Что лучше для WordPress: Nginx или Apache?","Оба подходят. Nginx экономнее по памяти, но правила .htaccess придётся переписывать в конфиг Nginx."),
("Как перенести существующий сайт на VPS?","Сделайте дамп базы (mysqldump), скопируйте каталог сайта через rsync, импортируйте базу и поправьте данные в wp-config.php."),
]))

D.append(dict(
slug="n8n-na-vps",
title="n8n на VPS: установка через Docker Compose, домен и HTTPS",
h1="n8n на своём VPS: свой сервер для автоматизаций",
desc="Как установить n8n на VPS через Docker Compose: конфиг, постоянное хранение данных, Nginx с поддержкой WebSocket, SSL, резервное копирование и контролируемые обновления.",
kw="n8n на vps, установка n8n docker, n8n self-hosted, автоматизация n8n сервер",
date="2026-11-05",
body=f'''
<p>n8n — конструктор автоматизаций, который можно развернуть у себя. Ресурсы и число параллельных запусков ограничены конфигурацией сервера; функции зависят от редакции и лицензии n8n. Нужен VPS с Docker, от 2 ГБ RAM и 1–2 ядер; установка Docker описана в <a href="/articles/docker-na-vps/">этом гайде</a>.</p>

<h2>1. Каталог и compose-файл</h2>
<pre><code>mkdir -p ~/n8n &amp;&amp; cd ~/n8n
nano compose.yaml</code></pre>
<pre><code>services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: unless-stopped
    ports:
      - "127.0.0.1:5678:5678"
    environment:
      - N8N_HOST=n8n.example.com
      - N8N_PROTOCOL=https
      - N8N_PORT=5678
      - N8N_WEBHOOK_URL=https://n8n.example.com/
      - N8N_PROXY_HOPS=1
      - GENERIC_TIMEZONE=Europe/Moscow
      - TZ=Europe/Moscow
    volumes:
      - n8n_data:/home/node/.n8n
volumes:
  n8n_data:</code></pre>
<pre><code>docker compose up -d
docker compose logs -f n8n</code></pre>
<p>Порт привязан к <code>127.0.0.1</code>, поэтому снаружи n8n недоступен напрямую. Наружу его выведет Nginx.</p>

<h2>2. Домен и обратный прокси</h2>
<p>Создайте A-запись <code>n8n.example.com</code> на IP сервера и конфиг Nginx. Обратите внимание на заголовки для WebSocket — без них редактор работает нестабильно:</p>
<pre><code>server {{
    listen 80;
    server_name n8n.example.com;
    location / {{
        proxy_pass http://127.0.0.1:5678;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
    }}
}}</code></pre>
<pre><code>sudo nginx -t &amp;&amp; sudo systemctl reload nginx
sudo certbot --nginx -d n8n.example.com</code></pre>
<p>Откройте адрес в браузере и создайте владельца аккаунта. Пример переменных рассчитан на n8n 2.35+: N8N_WEBHOOK_URL заменяет устаревшую WEBHOOK_URL. Перед рабочим запуском зафиксируйте проверенную версию образа. <a href="https://docs.n8n.io/hosting/configuration/configuration-examples/webhook-url/">Официальная документация n8n</a>.</p>

{cta("n8n удобно держать на отдельном небольшом VPS")}

<h2>3. Обновление</h2>
<pre><code>cd ~/n8n
docker compose pull
docker compose up -d
docker image prune -f</code></pre>

<h2>4. Бэкап</h2>
<p>Все воркфлоу и учётные данные лежат в томе <code>n8n_data</code>. Сделайте копию:</p>
<pre><code>docker compose stop n8n
docker run --rm -v n8n_n8n_data:/data:ro -v "$PWD":/backup alpine tar czf /backup/n8n-$(date +%F).tar.gz -C /data .
docker compose start n8n</code></pre>
<p>Подробнее о регулярных копиях — в статье про <a href="/articles/bekapy-vps-restic-rsync/">бэкапы VPS</a>. Перед копированием обязательно проверьте код завершения команды и реальное имя тома: неверное имя создаст пустой том и бесполезную копию. Имя тома может иметь префикс проекта (<code>n8n_n8n_data</code>), посмотрите <code>docker volume ls</code>.</p>

<h2>Типичные проблемы</h2>
<ul>
<li>Вебхуки открываются по неверному адресу — проверьте <code>WEBHOOK_URL</code>.</li>
<li>Редактор «зависает» — в Nginx нет заголовков Upgrade/Connection.</li>
<li>Не хватает памяти — добавьте swap или увеличьте тариф.</li>
</ul>
''',
faq=[
("Сколько ресурсов нужно для n8n?","Для личных и небольших рабочих сценариев достаточно 1–2 ядер и 2 ГБ RAM."),
("Нужен ли домен для n8n?","Для вебхуков от внешних сервисов нужен публичный адрес с HTTPS, то есть домен и сертификат."),
("Как не потерять данные при обновлении?","Храните данные в именованном томе Docker и делайте копию перед каждым обновлением."),
]))

D.append(dict(
slug="uptime-kuma-monitoring-vps",
title="Мониторинг сайтов и серверов: Uptime Kuma на VPS с уведомлениями в Telegram",
h1="Uptime Kuma на VPS: следим за сайтами и получаем алерты в Telegram",
desc="Как установить Uptime Kuma на VPS через Docker: мониторинг сайтов и портов, уведомления в Telegram, Nginx с WebSocket и SSL, публичная страница статуса.",
kw="uptime kuma установка, мониторинг сайта, мониторинг vps, уведомления telegram",
date="2026-11-05",
body=f'''
<p>Uptime Kuma — лёгкий бесплатный сервис мониторинга: проверяет сайты, порты, ping и присылает уведомление, когда что-то упало. Ему хватает минимального сервера: 1 ядро и 512 МБ – 1 ГБ RAM. Лучше разместить его на отдельном VPS, чем на том же сервере, который он проверяет.</p>

<h2>1. Запуск через Docker</h2>
<pre><code>docker run -d --restart=always \\
  -p 127.0.0.1:3001:3001 \\
  -v uptime-kuma:/app/data \\
  --name uptime-kuma \\
  louislam/uptime-kuma:1</code></pre>
<p>Установка Docker: <a href="/articles/docker-na-vps/">гайд</a>. Порт привязан к localhost, наружу откроем его через Nginx.</p>

<h2>2. Nginx и SSL</h2>
<pre><code>server {{
    listen 80;
    server_name status.example.com;
    location / {{
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}</code></pre>
<pre><code>sudo nginx -t &amp;&amp; sudo systemctl reload nginx
sudo certbot --nginx -d status.example.com</code></pre>
<p>Откройте адрес и создайте учётную запись администратора.</p>

<h2>3. Первый монитор</h2>
<ol>
<li>Нажмите <b>Add New Monitor</b>.</li>
<li>Тип <b>HTTP(s)</b>, URL вашего сайта, интервал 60 секунд.</li>
<li>Для сервера добавьте монитор типа <b>Ping</b> или <b>TCP Port</b> (например, 22 или 443).</li>
</ol>

<h2>4. Уведомления в Telegram</h2>
<ol>
<li>В Telegram создайте бота у @BotFather и получите токен.</li>
<li>Напишите боту любое сообщение и узнайте свой chat ID (например, через @userinfobot).</li>
<li>В Uptime Kuma: Settings → Notifications → Setup Notification → Telegram. Вставьте токен и chat ID, нажмите Test.</li>
<li>Включите уведомление «по умолчанию для новых мониторов».</li>
</ol>

{cta("Монитор лучше держать на отдельном сервере")}

<h2>5. Страница статуса</h2>
<p>В разделе Status Pages можно создать публичную страницу со списком сервисов и привязать её к домену. Удобно для клиентов.</p>

<h2>6. Обновление и бэкап</h2>
<pre><code>docker pull louislam/uptime-kuma:1
docker rm -f uptime-kuma
# затем повторите docker run из шага 1 — данные хранятся в томе uptime-kuma</code></pre>
<p>Не забывайте делать <a href="/articles/bekapy-vps-restic-rsync/">копии тома</a>.</p>
''',
faq=[
("Можно ли мониторить сайт, который на том же сервере?","Можно, но если упадёт сам сервер, упадёт и мониторинг. Надёжнее размещать Uptime Kuma отдельно."),
("Как часто проверять сайт?","Интервал 60 секунд — хороший баланс. Реже проверять нет смысла, чаще — лишняя нагрузка."),
]))
