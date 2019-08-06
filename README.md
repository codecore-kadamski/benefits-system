# benefits-system
Benefits System microservices


1. Lokalnie instalujemy Nginx

Aby móc lokanie na porcie 80 mieć serwis należy dodać wpis do /etc/nginx/nginx.conf

    server {
       listen     benefits.adamski.local:80;
       server_name     benefits.adamski.local;

        location / {
            auth_basic off;
            proxy_set_header X-Real-IP  $remote_addr;
            proxy_set_header X-Forwarded-For $remote_addr;
            proxy_set_header Host $host;
            proxy_pass http://127.0.0.1:13021;
        }
    }

Aby loklanie nam działał adres benefits.adamski.local musimy dodac wpis do /etc/hosts

127.0.0.1   benefits.adamski.local

oczywiście jest to domena umowna

2. Klonujemy projekt z https://github.com/codecore-kadamski/benefits-system

3. Wymagania projektu

Nie musimy mieć zainstalowanego serwera postgres, ale wymagane do uruchomienia są:

- docker
- docker-compose
- poetry
- pyenv

4. Menu poleceń

    W katalogu głównym mamy plik Makefile, tam mamy główne menu komend do zarzadzania projektem
    W poszczególnych aplikacjach: front, auths_domain również są Makefile z komendami powiązanymi z daną aplikacją

    start                 start project in containers
    stop                  stop project
    docker-rmi            usuwanie obrazów 
    docker-rm             usuwanie kontenerów


5. Infrastruktura projektu

    Mikro usługi:

    - front - aplikacja w Django, ale można zrobić w dowolnej technologi, by obsługiwało protokuł REST API, wydaje się że łatwiej we Flask, a najlepiej czysty HTML i Vue, Bulma jako CSS

    - front_nginx - proxy dla frontu

    - auths_domain - aplikacja we Flasku, domena autentykacji i autoryzacji. Także domena kont użytkowników

    - postgres - baza danych jedna dla wszystkich domen

Przyklad docker ps:

b4fa75f77c89        auths_domain:latest   "gunicorn -c gunicor…"   39 minutes ago      Up 39 minutes       0.0.0.0:5000->5000/tcp   auths_domain
d532560f5dc1        front_nginx:latest    "/etc/nginx/wait-for…"   39 minutes ago      Up 39 minutes       0.0.0.0:13021->80/tcp    front_nginx
b2fc6174adf0        postgres:9.6-alpine   "docker-entrypoint.s…"   39 minutes ago      Up 39 minutes       0.0.0.0:5432->5432/tcp   psqldb
9ad13f815f6d        front:latest          "gunicorn wsgi:appli…"   39 minutes ago      Up 39 minutes       8000/tcp                 front


5. Konfiguracja projektu



6. Uruchomienie projektu

    Środowisko lokalne - bez mikroserwisów

    - możliwe ale wymaga instalowania serwera postgres

    Środowisko lokalne - postgres jako mikroserwis

    - wymaga zakomentowania w docker-compose uruchamiania innych dockerów oprócz bazy danych

    Środowisko lokalne - mikroserwisy

    - najfajniej działa, uruchamiamy komenda: make start. 

        Docker buduje kontenery i uruchamia usługi, nginx jako proxy miedzy front mikroserwisu a portem 80 przeglądarki


7. Auths_domain

    Komendy make :

    migrations-prod       migracje produkcyjne w bazie postgres
    migrations-test       migracje testowe w sqlite
    start-local-server    start local server
    build                 buduje obraz kontenera
    run                   uruchamia  aplikacje w dokerze
    stop                  zatrzymuje kontener
    develop               poetry install requirements
    test                  uruchamiamy testy
    docker-rmi            usuwanie obrazów 
    docker-rm             usuwanie kontenerów


8. Gdy wszystko zostało uruchomione

    Mamy pustą bazę bez tabel, zatem należy:

    - w auths_domain uruchamiamy migracje produkcyjne

            make migrations-prod