from articles1 import cta, REF
E = []

E.append(dict(
slug="bekapy-vps-restic-rsync",
title="Бэкапы VPS: restic, rsync и cron — как настроить резервное копирование",
h1="Бэкапы VPS: автоматические копии с restic и rsync",
desc="Как настроить резервное копирование VPS: правило 3-2-1, rsync, шифрованные инкрементные бэкапы restic, дамп MySQL и PostgreSQL, расписание в cron и проверка восстановления.",
kw="бэкап vps, резервное копирование сервера, restic, rsync cron, бэкап mysql",
date="2026-11-05",
body=f'''
<p>Бэкап, который не проверяли на восстановление, — это надежда, а не бэкап. Сервер может сломаться из-за ошибки при обновлении, взлома, удаления файла или проблем хостера. Настроить копии нужно в первый день работы. Основа — правило <b>3-2-1</b>: три копии данных, на двух разных носителях, одна из них вне площадки сервера.</p>

<h2>Что копировать</h2>
<ul>
<li>каталоги проектов и сайтов (<code>/var/www</code>, <code>~/app</code>);</li>
<li>конфиги (<code>/etc/nginx</code>, <code>/etc/wireguard</code>, unit-файлы systemd);</li>
<li>дампы баз данных (а не сырые файлы работающей БД);</li>
<li>тома Docker с данными.</li>
</ul>
<p>Саму операционную систему копировать не нужно: её проще развернуть заново.</p>

<h2>Вариант 1: простой rsync</h2>
<p>Копирует только изменения на другой сервер по SSH:</p>
<pre><code>rsync -az --delete -e ssh /var/www/ backup@BACKUP_HOST:/backups/www/</code></pre>
<p>Минус: <code>--delete</code> повторяет и ошибочные удаления, истории версий нет.</p>

<h2>Вариант 2: restic — шифрованные версии</h2>
<p>restic делает инкрементные снимки, шифрует их и хранит дубли эффективно. Подходит SFTP, S3-совместимое хранилище и другой VPS.</p>
<pre><code>sudo apt install -y restic
echo 'ДЛИННЫЙ_ПАРОЛЬ_РЕПОЗИТОРИЯ' | sudo tee /root/.restic-pass &gt; /dev/null
sudo chmod 600 /root/.restic-pass
export RESTIC_REPOSITORY=sftp:backup@BACKUP_HOST:/backups/vps1
export RESTIC_PASSWORD_FILE=/root/.restic-pass
sudo -E restic init</code></pre>
<p>Запомните пароль репозитория отдельно: без него данные не восстановить.</p>

<h2>Скрипт бэкапа</h2>
<pre><code>sudo nano /usr/local/bin/backup.sh</code></pre>
<pre><code>#!/bin/bash
set -euo pipefail
export RESTIC_REPOSITORY=sftp:backup@BACKUP_HOST:/backups/vps1
export RESTIC_PASSWORD_FILE=/root/.restic-pass

mkdir -p /var/backups/db
mysqldump --single-transaction --all-databases | gzip &gt; /var/backups/db/mysql.sql.gz
# для PostgreSQL: sudo -u postgres pg_dumpall | gzip &gt; /var/backups/db/pg.sql.gz

restic backup /var/www /etc /home /var/backups/db --exclude-caches
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune</code></pre>
<pre><code>sudo chmod +x /usr/local/bin/backup.sh</code></pre>

<h2>Расписание в cron</h2>
<pre><code>sudo crontab -e
# каждый день в 03:30
30 3 * * * /usr/local/bin/backup.sh &gt;&gt; /var/log/backup.log 2&gt;&amp;1</code></pre>

{cta("Для копий удобен второй небольшой VPS в другой локации")}

<h2>Проверка восстановления</h2>
<pre><code>restic snapshots
restic restore latest --target /tmp/restore-test --include /etc/nginx
restic check</code></pre>
<p>Раз в месяц восстанавливайте тестовый файл. Только так вы узнаете, что копии рабочие.</p>

<h2>Снапшоты хостера</h2>
<p>Снапшоты в панели — хороший способ вернуться после неудачного обновления, но они лежат у того же провайдера. Считайте их дополнением к бэкапу, а не заменой.</p>
''',
faq=[
("Как часто делать бэкап?","Для большинства проектов раз в сутки. Для активных баз данных — чаще, ориентируясь на то, сколько данных вы готовы потерять."),
("Чем restic лучше rsync?","restic хранит версии, шифрует данные и экономит место за счёт дедупликации, а rsync просто синхронизирует каталоги."),
("Нужно ли копировать Docker-образы?","Нет, достаточно compose-файлов и томов с данными. Образы скачиваются заново."),
]))

E.append(dict(
slug="vps-tormozit-diagnostika",
title="VPS тормозит: как найти причину — CPU, память, диск и сеть",
h1="VPS тормозит: диагностика за 10 минут",
desc="Что делать, если VPS тормозит или завис: команды top, htop, free, iostat, df, ss и journalctl, поиск процессов-пожирателей, OOM-killer, нехватка диска и чужие нагрузки.",
kw="vps тормозит, высокая загрузка cpu linux, нехватка памяти oom, диагностика сервера",
date="2026-11-05",
body=f'''
<p>Сервер отвечает медленно? Не спешите менять тариф. Обычно причина находится за несколько минут одной из пяти групп команд: процессор, память, диск, сеть, логи.</p>

<h2>1. Общая картина: top и htop</h2>
<pre><code>uptime
top        # или: sudo apt install -y htop &amp;&amp; htop</code></pre>
<p>Что смотреть:</p>
<ul>
<li><b>load average</b> (три числа) — если он стабильно выше числа ядер, сервер перегружен;</li>
<li><b>%CPU</b> процессов — кто занимает процессор;</li>
<li><b>wa</b> (ожидание диска) — высокое значение значит, что тормозит диск;</li>
<li><b>st</b> (steal) — процессор «украден» соседями по физическому серверу, это повод обратиться к хостеру.</li>
</ul>

<h2>2. Память</h2>
<pre><code>free -h
ps aux --sort=-%mem | head -10</code></pre>
<p>Если свободной памяти почти нет, а swap активно используется, система работает медленно. Проверьте, не срабатывал ли OOM-killer:</p>
<pre><code>sudo dmesg -T | grep -i -E 'killed process|out of memory'
journalctl -k | grep -i oom</code></pre>
<p>Решения: оптимизировать приложение, <a href="/articles/nastroika-ubuntu-vps/">добавить swap</a>, перейти на тариф с большим объёмом RAM.</p>

<h2>3. Диск</h2>
<pre><code>df -h
sudo du -xh / --max-depth=2 2&gt;/dev/null | sort -h | tail -15
df -i</code></pre>
<p>Если диск заполнен на 100%, перестают работать базы данных и логи. Частые виновники: логи в <code>/var/log</code>, образы Docker, старые бэкапы. Очистка:</p>
<pre><code>sudo journalctl --vacuum-size=200M
sudo apt clean
docker system prune -af    # осторожно: удаляет неиспользуемые образы</code></pre>
<p>Для нагрузки на диск: <code>sudo apt install -y iotop sysstat</code> и затем <code>sudo iotop -o</code> или <code>iostat -x 2</code>.</p>

<h2>4. Сеть и порты</h2>
<pre><code>ss -tulpn          # кто слушает порты
ss -s              # сводка по соединениям
sudo apt install -y iftop &amp;&amp; sudo iftop</code></pre>
<p>Большое число соединений может означать наплыв ботов или атаку. Включите <a href="/articles/nastroika-ubuntu-vps/">fail2ban и файрвол</a>, ограничьте запросы в Nginx через <code>limit_req</code>.</p>

<h2>5. Логи служб</h2>
<pre><code>systemctl --failed
journalctl -p err -b --no-pager | tail -50
journalctl -u nginx --since "1 hour ago"</code></pre>

<h2>6. Подозрительные процессы</h2>
<p>Если процесс с непонятным именем занимает весь процессор, проверьте:</p>
<pre><code>ps aux --sort=-%cpu | head
sudo ls -l /proc/PID/exe
last -a | head ; sudo lastb | head
crontab -l ; sudo ls /etc/cron.d</code></pre>
<p>При признаках взлома (чужие входы, незнакомые cron-задания) безопаснее переустановить сервер и восстановить данные из <a href="/articles/bekapy-vps-restic-rsync/">бэкапа</a>, сменив все пароли и ключи.</p>

{cta("Если упёрлись в ресурсы, проще перейти на тариф мощнее")}

<h2>Быстрая шпаргалка</h2>
<table><thead><tr><th>Симптом</th><th>Проверить</th><th>Решение</th></tr></thead><tbody>
<tr><td>Высокий load, wa малый</td><td>top, ps</td><td>оптимизация или больше ядер</td></tr>
<tr><td>Высокий wa</td><td>iotop, iostat</td><td>найти процесс, NVMe, кэш</td></tr>
<tr><td>Мало свободной RAM</td><td>free, dmesg</td><td>swap, лимиты, больше RAM</td></tr>
<tr><td>Диск 100%</td><td>df, du</td><td>очистка логов и образов</td></tr>
<tr><td>Высокий st</td><td>top</td><td>обратиться к хостеру</td></tr>
</tbody></table>
''',
faq=[
("Что значит высокий load average?","Это среднее число процессов, ожидающих процессор или диск. Если он стабильно выше числа ядер, сервер перегружен."),
("Что такое steal в top?","Доля времени, когда виртуальный процессор не получил ресурсов от гипервизора. Постоянно высокий steal — повод написать в поддержку хостера."),
("Почему сервер упал без причины?","Часто это OOM-killer: ядро убило процесс из-за нехватки памяти. Следы ищите командой dmesg -T | grep -i oom."),
]))

E.append(dict(
slug="vaultwarden-na-vps",
title="Vaultwarden на VPS: свой менеджер паролей, совместимый с Bitwarden",
h1="Vaultwarden на VPS: собственный менеджер паролей",
desc="Как развернуть Vaultwarden (совместимый с Bitwarden сервер) на VPS через Docker Compose: домен, HTTPS, отключение открытой регистрации, админ-панель и бэкап.",
kw="vaultwarden установка, свой менеджер паролей, bitwarden self-hosted, vaultwarden docker",
date="2026-11-05",
body=f'''
<p>Vaultwarden — лёгкая реализация сервера Bitwarden. Вы получаете свой менеджер паролей с приложениями для телефона, расширениями для браузера и общим доступом для семьи. Серверу хватит минимального VPS: 1 ядро и 512 МБ – 1 ГБ RAM. Но хранилище паролей — критичный сервис, поэтому сначала <a href="/articles/nastroika-ubuntu-vps/">защитите сервер</a>.</p>

<h2>Важно знать заранее</h2>
<ul>
<li>Работает только через HTTPS (без него клиенты Bitwarden не подключатся).</li>
<li>Вы отвечаете за обновления и бэкапы. Потеря базы без копии = потеря паролей.</li>
<li>Не размещайте сервис без регулярных <a href="/articles/bekapy-vps-restic-rsync/">бэкапов</a>.</li>
</ul>

<h2>1. Docker Compose</h2>
<p>Docker ставится по <a href="/articles/docker-na-vps/">этой инструкции</a>.</p>
<pre><code>mkdir -p ~/vaultwarden &amp;&amp; cd ~/vaultwarden
nano compose.yaml</code></pre>
<pre><code>services:
  vaultwarden:
    image: vaultwarden/server:latest
    restart: unless-stopped
    environment:
      DOMAIN: "https://vault.example.com"
      SIGNUPS_ALLOWED: "true"
    volumes:
      - ./vw-data:/data
    ports:
      - "127.0.0.1:8080:80"</code></pre>
<pre><code>docker compose up -d</code></pre>

<h2>2. Nginx и сертификат</h2>
<pre><code>server {{
    listen 80;
    server_name vault.example.com;
    client_max_body_size 128M;
    location / {{
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}</code></pre>
<pre><code>sudo nginx -t &amp;&amp; sudo systemctl reload nginx
sudo certbot --nginx -d vault.example.com</code></pre>

<h2>3. Регистрация и закрытие регистрации</h2>
<ol>
<li>Откройте <code>https://vault.example.com</code> и создайте свою учётную запись с длинным мастер-паролем.</li>
<li>Измените в compose-файле <code>SIGNUPS_ALLOWED: "false"</code>.</li>
<li>Примените: <code>docker compose up -d</code>.</li>
</ol>
<p>Теперь новых пользователей можно добавлять только приглашением.</p>

<h2>4. Подключение клиентов</h2>
<p>В приложении Bitwarden (телефон, браузер, ПК) на экране входа нажмите «Self-hosted» и введите адрес сервера. Включите двухфакторную аутентификацию в настройках аккаунта.</p>

{cta("Для менеджера паролей подойдёт самый скромный тариф")}

<h2>5. Бэкап и обновление</h2>
<pre><code># копия данных
tar czf ~/vw-backup-$(date +%F).tar.gz -C ~/vaultwarden vw-data

# обновление
docker compose pull &amp;&amp; docker compose up -d</code></pre>
<p>Храните копию вне сервера и периодически проверяйте восстановление.</p>
''',
faq=[
("Vaultwarden безопасен?","При правильной настройке (HTTPS, длинный мастер-пароль, 2FA, обновления) да. Но безопасность сервера и бэкапов — ваша ответственность."),
("Нужны ли для Vaultwarden большие ресурсы?","Нет, он очень лёгкий и работает на минимальном VPS."),
("Что будет, если сервер недоступен?","Клиенты Bitwarden хранят локальную копию хранилища и работают офлайн, но без синхронизации."),
]))

E.append(dict(
slug="fastapi-na-vps",
title="FastAPI на VPS: Uvicorn, systemd, Nginx и HTTPS для продакшена",
h1="Деплой FastAPI на VPS: Uvicorn + systemd + Nginx",
desc="Как развернуть FastAPI-приложение на VPS: виртуальное окружение, запуск через systemd, обратный прокси Nginx, SSL Let's Encrypt, переменные окружения и обновление.",
kw="fastapi деплой vps, uvicorn systemd nginx, python приложение на сервере, развернуть fastapi",
date="2026-11-05",
body=f'''
<p>Для небольшого FastAPI-проекта достаточно VPS с 1 ядром и 1 ГБ RAM. Схема простая: Uvicorn запускает приложение на локальном порту, systemd следит за процессом, Nginx принимает внешний трафик по HTTPS. Подготовьте сервер по <a href="/articles/nastroika-ubuntu-vps/">базовой инструкции</a> и направьте домен на IP.</p>

<h2>1. Окружение</h2>
<pre><code>sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx git
mkdir -p ~/api &amp;&amp; cd ~/api
python3 -m venv venv
source venv/bin/activate
pip install fastapi "uvicorn[standard]"</code></pre>

<h2>2. Пример приложения</h2>
<pre><code>cat &gt; main.py &lt;&lt;'EOF'
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {{"status": "ok"}}
EOF
uvicorn main:app --host 127.0.0.1 --port 8000</code></pre>
<p>Проверьте в другой сессии: <code>curl http://127.0.0.1:8000/health</code>. Остановите сервер (Ctrl+C).</p>

<h2>3. Запуск через systemd</h2>
<pre><code>sudo nano /etc/systemd/system/api.service</code></pre>
<pre><code>[Unit]
Description=FastAPI app
After=network.target

[Service]
User=deploy
WorkingDirectory=/home/deploy/api
EnvironmentFile=-/home/deploy/api/.env
ExecStart=/home/deploy/api/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target</code></pre>
<pre><code>sudo systemctl daemon-reload
sudo systemctl enable --now api
sudo systemctl status api
journalctl -u api -f</code></pre>
<p>Количество воркеров подбирайте по числу ядер. Секреты храните в <code>.env</code> с правами 600.</p>

<h2>4. Nginx как обратный прокси</h2>
<pre><code>server {{
    listen 80;
    server_name api.example.com;
    location / {{
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}</code></pre>
<pre><code>sudo nginx -t &amp;&amp; sudo systemctl reload nginx
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.example.com</code></pre>

{cta("Для API на Python хватит небольшого VPS")}

<h2>5. Обновление приложения</h2>
<pre><code>cd ~/api &amp;&amp; git pull
source venv/bin/activate &amp;&amp; pip install -r requirements.txt
sudo systemctl restart api</code></pre>

<h2>Советы для продакшена</h2>
<ul>
<li>Отключите <code>/docs</code> и <code>/openapi.json</code> для публичного API, если они не нужны: <code>FastAPI(docs_url=None, redoc_url=None)</code>.</li>
<li>Ограничьте частоту запросов через <code>limit_req</code> в Nginx.</li>
<li>Для базы данных используйте PostgreSQL и регулярные <a href="/articles/bekapy-vps-restic-rsync/">бэкапы</a>.</li>
<li>Следите за доступностью через <a href="/articles/uptime-kuma-monitoring-vps/">Uptime Kuma</a>.</li>
</ul>
''',
faq=[
("Нужен ли Gunicorn для FastAPI?","Не обязательно: Uvicorn с параметром --workers подходит для большинства проектов. Gunicorn с воркерами Uvicorn используют для более тонкого управления процессами."),
("Сколько воркеров ставить?","Ориентир — по одному на ядро. Для лёгких API на 1 ядре достаточно 1–2."),
]))
