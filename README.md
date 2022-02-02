# EventAPI
RESTAPI do aplikacji Events Calendar.


# Instalacja
<li>instalacja potrzebnych pakietów:
<pre><code>python -m pip install -r .\requirements.txt</code></pre>
<li>edycja pliku Config.ini do połączenia z bazą
<pre><code>[postgresql]
host = localhost
database = lectures
user = postgres
password = postgres</code></pre>

<p><b>host</b> = adres ip bazy danych
<p><b>database</b> = nazwa bazy danych
<p><b>user</b> = nazwa użytkownika bazy danych
<p><b>password</b> = hasło do użytkownika bazy danych

# Uruchomienie
Aby uruchomić api wpisujemy:
<pre><code>python server.py</code></pre>
jeżeli wszystko dobrze skonfigurujemy to otrzymamy taki widok:
<pre><code> _____                      _            _     ____   ___ 
| ____|__   __  ___  _ __  | |_  ___    / \   |  _ \ |_ _|
|  _|  \ \ / / / _ \| '_ \ | __|/ __|  / _ \  | |_) | | |
| |___  \ V / |  __/| | | || |_ \__ \ / ___ \ |  __/  | |
|_____|  \_/   \___||_| |_| \__||___//_/   \_\|_|    |___|


▌│█║▌║▌║     version: 1.0.4 created by dannyx-hub    ║▌║▌║█│▌

github: https://github.com/dannyx-hub

* Connected to Database
</code></pre>