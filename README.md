# EventAPI
RESTAPI do aplikacji Events Calendar.


# Instalacja
<li>instalacja potrzebnych pakietów:
<pre><code>python -m pip install -r .\requirements.txt</code></pre>
<li>edycja pliku Config.ini do ustawienia parametrów działania aplikacji
<pre><code>[postgresql]
host = localhost
database = lectures
user = postgres
password = postgres
<br>
[email]
server =
port = 
username = 
password = 
tls = 
ssl = 
<br>
[app]
debug = 
secret_key = 
</pre></code>
  <h3>[postgres]</h3>
<p><b>host</b> = adres ip bazy danych
<p><b>database</b> = nazwa bazy danych
<p><b>user</b> = nazwa użytkownika bazy danych
<p><b>password</b> = hasło do użytkownika bazy danych

<h3>[postgres]</h3>
 <p><b>server</b> = nazwa serwera smtp
  <p><b>port</b> = port serwera smtp
    <p><b>username</b> = nazwa użytkownika
      <p><b>password</b> = hasło użytkownika
        <p><b>tls</b> = ustawienie tls
          <p><b>ssl</b> = ustawienie ssl
  <h3>[app]</h3>
  <p><b>debug</b> = tryb debugowania (domyślnie false)
  <p><b>secret_key</b> = klucz do szyfrowania tokenu
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
