from articles1 import cta, REF
C = []

C.append(dict(
slug="docker-na-vps",
title="Docker на VPS: установка, docker compose и автозапуск контейнеров",
h1="Docker на VPS: установка и первый проект на compose",
desc="Как установить Docker и Docker Compose на Ubuntu VPS, запустить контейнеры с автоперезапуском, ограничить ресурсы и не забить диск образами.",
kw="docker на vps, установка docker ubuntu, docker compose, контейнеры на сервере",
date="2026-11-05",
body=f'''
<p>Docker упрощает развёртывание: приложение, база данных и зависимости упакованы в контейнеры, а переезд на другой сервер занимает минуты. Для комфортной работы с несколькими контейнерами берите VPS от 2 ядер и 2 ГБ RAM.</p>

<h2>1. Установка Docker из официального репозитория</h2>
<pre><code>sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release &amp;&amp; echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER</code></pre>
<p>Перезайдите по SSH, чтобы применилась группа, и проверьте: <code>docker run --rm hello-world</code>.</p>

<h2>2. Первый проект на docker compose</h2>
<p>Пример: веб-сервер Nginx и база PostgreSQL.</p>
<pre><code>mkdir ~/app &amp;&amp; cd ~/app
nano compose.yaml</code></pre>
<pre><code>services:
  web:
    image: nginx:stable
    ports:
      - "80:80"
    restart: unless-stopped
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: ${{DB_PASSWORD}}
    volumes:
      - dbdata:/var/lib/postgresql/data
    restart: unless-stopped
volumes:
  dbdata:</code></pre>
<pre><code>echo 'DB_PASSWORD=придумайте_длинный_пароль' &gt; .env
docker compose up -d
docker compose ps</code></pre>

<h2>3. Полезные команды</h2>
<pre><code>docker compose logs -f web      # логи
docker compose pull &amp;&amp; docker compose up -d   # обновить образы
docker compose down             # остановить
docker stats                    # потребление ресурсов</code></pre>

<h2>4. Не забивайте диск</h2>
<p>Старые образы и кэш сборки быстро занимают гигабайты:</p>
<pre><code>docker system df
docker system prune -af --volumes   # осторожно: удаляет неиспользуемые тома</code></pre>
<p>Ограничьте размер логов контейнеров в <code>/etc/docker/daemon.json</code>:</p>
<pre><code>{{
  "log-driver": "json-file",
  "log-opts": {{ "max-size": "10m", "max-file": "3" }}
}}</code></pre>

{cta("Docker любит память и быстрый диск")}

<h2>5. Важное про безопасность</h2>
<ul>
<li>Docker публикует порты в обход UFW. Привязывайте служебные порты к localhost: <code>"127.0.0.1:5432:5432"</code>.</li>
<li>Не запускайте контейнеры с <code>--privileged</code> без необходимости.</li>
<li>Секреты храните в <code>.env</code> с правами 600, не в репозитории.</li>
</ul>
<p>Для публикации сайтов используйте обратный прокси: <a href="/articles/sajt-na-vps-nginx-ssl/">Nginx и Let's Encrypt</a>.</p>
''',
faq=[
("Сколько RAM нужно для Docker?","Сам Docker лёгкий, ресурсы зависят от контейнеров. Для пары сервисов с базой данных комфортно от 2 ГБ."),
("Почему UFW не закрывает порт контейнера?","Docker сам управляет правилами iptables. Публикуйте порты на 127.0.0.1 и выводите наружу только через обратный прокси."),
]))

C.append(dict(
slug="minecraft-server-na-vps",
title="Minecraft-сервер на VPS: Java, Paper, systemd и сколько ресурсов нужно",
h1="Свой Minecraft-сервер на VPS: от установки до автозапуска",
desc="Как создать Minecraft-сервер на VPS с Ubuntu: установка Java, запуск Paper, настройка RAM, whitelist, автозапуск через systemd и бэкапы.",
kw="minecraft сервер на vps, как создать сервер майнкрафт, paper server ubuntu, хостинг майнкрафт",
date="2026-11-05",
body=f'''
<p>Свой сервер Minecraft даёт полный контроль над плагинами, миром и правилами. Платформа Paper — быстрая форк-версия ванильного сервера с поддержкой плагинов. Ниже установка на Ubuntu VPS.</p>

<h2>Какие ресурсы нужны</h2>
<table><thead><tr><th>Игроков</th><th>RAM</th><th>CPU</th></tr></thead><tbody>
<tr><td>1–5 (ваниль)</td><td>2–3 ГБ</td><td>2 ядра</td></tr>
<tr><td>5–15 + плагины</td><td>4–6 ГБ</td><td>2–4 ядра</td></tr>
<tr><td>15+ или моды</td><td>8 ГБ+</td><td>4+ ядра</td></tr>
</tbody></table>
<p>Minecraft сильно нагружает <b>одно</b> ядро, поэтому важна высокая частота процессора, а не их количество. Диск лучше NVMe — мир грузится быстрее. Выбирайте локацию ближе к игрокам. Подробнее — в <a href="/articles/kak-vybrat-vps/">чек-листе выбора VPS</a>.</p>

<h2>1. Установите Java</h2>
<p>Современные версии Minecraft требуют Java 21 (проверьте требование вашей версии):</p>
<pre><code>sudo apt update
sudo apt install -y openjdk-21-jre-headless
java -version</code></pre>

<h2>2. Отдельный пользователь и папка</h2>
<pre><code>sudo adduser --system --group --home /opt/minecraft minecraft
sudo -u minecraft mkdir -p /opt/minecraft/server
cd /opt/minecraft/server</code></pre>

<h2>3. Скачайте Paper</h2>
<p>Свежий jar-файл берите на официальном сайте PaperMC (papermc.io/downloads), сохраните как <code>paper.jar</code> в папку сервера и примите EULA:</p>
<pre><code>sudo -u minecraft sh -c 'echo "eula=true" &gt; /opt/minecraft/server/eula.txt'</code></pre>

<h2>4. Автозапуск через systemd</h2>
<pre><code>sudo nano /etc/systemd/system/minecraft.service</code></pre>
<pre><code>[Unit]
Description=Minecraft Server
After=network.target

[Service]
User=minecraft
WorkingDirectory=/opt/minecraft/server
ExecStart=/usr/bin/java -Xms2G -Xmx3G -jar paper.jar --nogui
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target</code></pre>
<pre><code>sudo systemctl daemon-reload
sudo systemctl enable --now minecraft
sudo ufw allow 25565/tcp</code></pre>
<p>Не отдавайте Java всю память VPS: оставьте 500 МБ – 1 ГБ системе.</p>

<h2>5. Защита сервера</h2>
<p>В <code>server.properties</code> включите <code>white-list=true</code> и <code>enforce-whitelist=true</code>, затем добавляйте игроков командой <code>whitelist add Ник</code> в консоли. Для публичных серверов пригодится DDoS-защита хостера.</p>

{cta("Для игрового сервера важны частота ядра и пинг")}

<h2>6. Бэкапы мира</h2>
<pre><code>sudo tar czf /root/world-$(date +%F).tar.gz -C /opt/minecraft/server world</code></pre>
<p>Положите команду в cron и храните копии вне сервера.</p>
''',
faq=[
("Сколько RAM нужно для Minecraft-сервера?","Для небольшой компании хватает 2–4 ГБ. Для плагинов и десятков игроков нужно 6–8 ГБ и больше."),
("Чем Paper лучше ванильного сервера?","Paper оптимизирован по производительности и поддерживает плагины Bukkit/Spigot."),
("Какой порт открывать?","Стандартный порт Minecraft Java Edition — 25565/tcp."),
]))

C.append(dict(
slug="vps-vs-vds-vs-hosting",
title="VPS, VDS, хостинг или выделенный сервер: в чём разница и что выбрать",
h1="VPS vs VDS vs виртуальный хостинг vs dedicated: что выбрать",
desc="Понятное сравнение VPS, VDS, виртуального хостинга и выделенного сервера: ресурсы, цена, сложность, безопасность и сценарии использования.",
kw="vps или хостинг, разница vps и vds, выделенный сервер или vps, что выбрать",
date="2026-11-05",
body=f'''
<p>Новички часто путаются в терминах: хостинг, VPS, VDS, облако, dedicated. Разберём простыми словами, когда что подходит.</p>

<h2>Виртуальный (shared) хостинг</h2>
<p>Вы арендуете место на общем сервере вместе с сотнями других сайтов. Панель управления, почта и поддержка уже настроены. <b>Плюсы:</b> просто, ничего не нужно администрировать. <b>Минусы:</b> нет root-доступа, жёсткие лимиты, соседи могут влиять на скорость, нельзя ставить свои программы. Подходит для визитки и простого WordPress.</p>

<h2>VPS / VDS</h2>
<p>Это виртуальная машина с выделенными ресурсами и полным root-доступом. Термины VPS и VDS на практике взаимозаменяемы: VDS чаще означает гарантированные ресурсы на KVM. <b>Плюсы:</b> свобода (Docker, боты, VPN, игровые серверы, любые сайты), предсказуемая производительность, масштабирование. <b>Минусы:</b> администрирование ложится на вас: обновления, защита, бэкапы.</p>

<h2>Выделенный сервер (dedicated)</h2>
<p>Физический сервер целиком ваш. <b>Плюсы:</b> максимум производительности, нет соседей. <b>Минусы:</b> заметно дороже, масштабирование сложнее. Нужен для высоконагруженных проектов, больших баз данных, рендеринга.</p>

<h2>Облако (cloud)</h2>
<p>Ресурсы оплачиваются по факту использования и легко масштабируются. Хорошо для проектов с непредсказуемой нагрузкой, но счета бывают сложно прогнозировать.</p>

<h2>Сводная таблица</h2>
<table><thead><tr><th></th><th>Хостинг</th><th>VPS/VDS</th><th>Dedicated</th></tr></thead><tbody>
<tr><td>Root-доступ</td><td>нет</td><td>да</td><td>да</td></tr>
<tr><td>Сложность</td><td>низкая</td><td>средняя</td><td>высокая</td></tr>
<tr><td>Цена</td><td>самая низкая</td><td>умеренная</td><td>высокая</td></tr>
<tr><td>Гибкость</td><td>низкая</td><td>высокая</td><td>максимальная</td></tr>
</tbody></table>

<h2>Как выбрать</h2>
<ul>
<li>Простой сайт-визитка без желания разбираться → хостинг.</li>
<li>Боты, VPN, Docker, свои сервисы, обучение администрированию → <b>VPS</b>.</li>
<li>Тяжёлая база данных, высокая нагрузка, большие объёмы → dedicated.</li>
</ul>
<p>Если выбрали VPS, переходите к <a href="/articles/kak-vybrat-vps/">чек-листу выбора</a> и <a href="/articles/nastroika-ubuntu-vps/">первичной настройке</a>.</p>

{cta("Хотите попробовать VPS без больших вложений?")}
''',
faq=[
("VPS дороже хостинга?","Обычно да, но разница небольшая, а возможности несопоставимы: root-доступ, любые программы, свои настройки."),
("Нужно ли уметь администрировать, чтобы взять VPS?","Базовые навыки Linux понадобятся, но гайды вроде нашей инструкции по первичной настройке закрывают основные задачи."),
]))

C.append(dict(
slug="aeza-obzor",
title="Хостинг Aeza: обзор, на что смотреть при заказе и кому подойдёт",
h1="Обзор Aeza: что нужно знать перед заказом VPS",
desc="Обзор VPS-хостинга Aeza: для каких задач подходит, на что обратить внимание при выборе тарифа и локации, как проверить сервер после выдачи.",
kw="aeza обзор, aeza хостинг отзывы, aeza vps, aeza.net",
date="2026-11-05",
body=f'''
<p>Aeza — один из популярных у русскоязычной аудитории провайдеров VPS и выделенных серверов. На рынке он известен виртуальными серверами в нескольких странах, быстрой выдачей и широким выбором локаций. Эта статья — практический взгляд: для каких задач сервис подходит, на что смотреть при заказе и как проверить сервер сразу после выдачи. Актуальные тарифы, характеристики и список локаций меняются, поэтому сверяйте их на <a href="{REF}" rel="sponsored nofollow noopener" target="_blank">официальном сайте Aeza</a>.</p>
<p><i>Раскрытие: ссылки на Aeza в этой статье партнёрские. Это не влияет на цену, а мнение здесь основано на критериях выбора, а не на рекламных обещаниях.</i></p>

<h2>Для каких задач подходит</h2>
<ul>
<li>Боты, парсеры, фоновые скрипты, которым нужна работа 24/7.</li>
<li>Личные сервисы: WireGuard, облако, менеджер паролей, панели мониторинга.</li>
<li>Сайты и проекты на Docker.</li>
<li>Игровые серверы (когда важны частота ядра и пинг).</li>
<li>Тестовые и учебные стенды для практики администрирования.</li>
</ul>

<h2>Что проверить перед заказом</h2>
<ol>
<li><b>Локация.</b> Для аудитории из России важен пинг, для зарубежных сервисов — расположение дата-центра. Выбирайте исходя из задачи.</li>
<li><b>Тип ресурсов.</b> Общие или выделенные ядра, тип диска (NVMe/SSD), скорость порта и условия по трафику.</li>
<li><b>Виртуализация и ОС.</b> Нужна ли вам KVM, какие образы ОС доступны, есть ли загрузка своего ISO.</li>
<li><b>Оплата.</b> Какие способы доступны, можно ли платить помесячно.</li>
<li><b>Правила использования (ToS).</b> Прочитайте, что запрещено: у любого хостера есть ограничения на рассылки, сканирование, нарушающий закон контент.</li>
<li><b>DDoS-защита.</b> Важна для игровых и публичных сервисов; уточните её уровень.</li>
</ol>

{cta("Сверьте актуальные тарифы и локации")}

<h2>Как проверить сервер после выдачи</h2>
<p>Сразу после получения выполните короткий тест. Он покажет реальный процессор, диск и сеть:</p>
<pre><code>lscpu | grep -E 'Model name|^CPU\\(s\\)'
free -h
df -h
curl -s https://ipinfo.io/json
# тест скорости диска
dd if=/dev/zero of=testfile bs=1M count=1024 oflag=direct; rm testfile
# тест сети (скачайте свой файл или используйте speedtest-cli)
sudo apt install -y speedtest-cli &amp;&amp; speedtest-cli</code></pre>
<p>Заодно проверьте IP-адрес: не находится ли он в чёрных списках и нормально ли открываются нужные вам сервисы.</p>

<h2>Плюсы и ограничения (общие критерии)</h2>
<table><thead><tr><th>Смотрите на</th><th>Хорошо, если</th><th>Осторожно, если</th></tr></thead><tbody>
<tr><td>Поддержка</td><td>отвечает быстро и по делу</td><td>долго молчит по критичным вопросам</td></tr>
<tr><td>Ресурсы</td><td>реальные показатели совпадают с тарифом</td><td>сильные просадки при нагрузке</td></tr>
<tr><td>Сеть</td><td>стабильный пинг и скорость</td><td>частые обрывы</td></tr>
<tr><td>Условия</td><td>понятные правила и возврат</td><td>скрытые лимиты</td></tr>
</tbody></table>
<p>Проверить всё это лучше всего на практике: берите минимальный срок оплаты, прогоните тесты выше и только потом переезжайте надолго.</p>

<h2>С чего начать после заказа</h2>
<ol>
<li><a href="/articles/nastroika-ubuntu-vps/">Защитите сервер</a>: ключи SSH, UFW, fail2ban.</li>
<li>Поднимите нужный сервис: <a href="/articles/telegram-bot-na-vps/">бот</a>, <a href="/articles/sajt-na-vps-nginx-ssl/">сайт</a>, <a href="/articles/wireguard-na-vps/">WireGuard</a> или <a href="/articles/docker-na-vps/">Docker</a>.</li>
<li>Настройте бэкапы.</li>
</ol>
''',
faq=[
("Aeza подходит новичкам?","Для новичков важны быстрая выдача сервера и понятная панель. Сверьте актуальные условия на официальном сайте и начните с минимального тарифа на месяц."),
("Как проверить качество VPS после покупки?","Проверьте процессор (lscpu), скорость диска (dd), сеть (speedtest-cli) и стабильность пинга. Это занимает 5 минут."),
("Где посмотреть актуальные цены?","Только на официальном сайте хостера: тарифы и акции меняются."),
]))
