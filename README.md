# FisherJournal - это сообщество в Телеграм, которое включает в себя 3 бота-помощника и сайт новостей о рыбалке.

![example workflow](https://github.com/DenisKtv/river_bot/actions/workflows/main.yml/badge.svg)  

## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![aiogram](https://img.shields.io/badge/-aiogram-2B6EDE?style=flat-square&logo=telegram)](https://aiogram.dev/)
[![HTML](https://img.shields.io/badge/-HTML-E34F26?style=flat-square&logo=HTML5&logoColor=white)](https://www.w3.org/TR/html52/)
[![CSS](https://img.shields.io/badge/-CSS-1572B6?style=flat-square&logo=CSS3&logoColor=white)](https://www.w3.org/Style/CSS/Overview.en.html)
[![Bootstrap](https://img.shields.io/badge/-Bootstrap-7952B3?style=flat-square&logo=Bootstrap&logoColor=white)](https://getbootstrap.com/)
[![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=JavaScript&logoColor=black)](https://www.ecma-international.org/publications/standards/Ecma-262.htm)
[![Prometheus](https://img.shields.io/badge/-Prometheus-E6522C?style=flat-square&logo=Prometheus&logoColor=white)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/-Grafana-F46800?style=flat-square&logo=Grafana&logoColor=white)](https://grafana.com/)

## Описание проекта

Первый бот предоставляет информацию по названию реки, озера или водохранилища: об уровне воды, ее температуре, паводках и детальном прогнозе погоды в данной точке. Дополнительно он выводит список доступных рек и озер по команде "список".

Второй бот подключен к API ChatGPT с вводными данными о том, что он - рыбак со стажем. Он предоставляет советы и информацию, связанную с рыбалкой.

Третий бот - администратор. Он удаляет лишние оповещения в группе, парсит новости с нашей новостной страницы и отправляет их в наше телеграм-сообщество. Также он выводит сообщения об успешном CI/CD и сообщения, отправленные через форму Обратной Связи с нашего сайта.
Все эти боты работают вместе, чтобы создать полноценное и удобное пространство для любителей рыбалки.

В рамках нашего проекта мы разработали компактный информационный новостной сайт. Он упакован в Docker контейнеры для обеспечения современной, безопасной и масштабируемой инфраструктуры.

Наш проект настроен таким образом, что мониторинг системы происходит в режиме реального времени с использованием инструментов Prometheus и Grafana. Это позволяет нам своевременно отслеживать любые изменения, улучшать производительность и обеспечивать безупречную работу системы.

Безопасность также является одним из наших приоритетов. Мы реализовали автоматическое обновление SSL сертификата с использованием Docker контейнера. Встроенный скрипт запускается ежедневно и перезагружает контейнер Nginx, обеспечивая своевременное обновление сертификатов и обеспечение безопасности ваших данных.

## Установка проекта локально

* Склонировать репозиторий на локальную машину:
```bash
git clone https://github.com/DenisKtv/river_bot.git
cd river_bot
```

* Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
. venv/bin/activate
```

* Cоздайте файл `.env` в директории `/infra/` с содержанием:

```
BOTS TOKENs:
TOKEN =
ADMIN_TOKEN = 
CHAT_TOKEN = 

Site:
URL = 

Django:
SECRET_KEY = 

telegram chat:
MY_CHAT = 
GROUP_ID =

OpenAi token:
AI_TOKEN =

Prometheus and Grafana:
ADMIN_USER = 
ADMIN_PASSWORD = 

Postgresql:
DB_ENGINE = 
DB_NAME = 
POSTGRES_USER = 
POSTGRES_PASSWORD = 
HOST = 
PORT = 
```

* Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

* Выполните миграции:

```bash
python manage.py migrate
```

* Запустите сервер:
```bash
python manage.py runserver
```

## Для запуска ботов локально:
Перейти в нужный репозиторий и запустить ботов:
```bash
cd bots/
python bot_chat.py
python admin_bot.py
python main.py
```

## Запуск проекта в Docker контейнере
* Установите Docker.

Параметры запуска описаны в файлах `docker-compose.yml` и `nginx.conf` которые находятся в директории `infra/`.  
При необходимости добавьте/измените адреса проекта в файле `nginx.conf`

* Запустите docker-compose:
```bash
docker-compose up -d --build
```  
  > После сборки появляются 3 контейнера:
  > 1. контейнер базы данных **db**
  > 2. контейнер приложения **web**
  > 3. контейнер web-сервера **nginx**
* Примените миграции:
```bash
docker-compose exec backend python manage.py migrate
```
* Создайте администратора:
```bash
docker-compose exec backend python manage.py createsuperuser
```
* Соберите статику:
```bash
docker-compose exec backend python manage.py collectstatic --no-input
```

## Сайт
Сайт доступен по ссылке:
[https://fisherjournal.xyz](https://fisherjournal.xyz)
Сообщество в телеграм:
[https://t.me/fish_journal](https://t.me/fish_journal)
