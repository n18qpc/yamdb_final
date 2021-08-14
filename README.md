# yamdb_final

Проект: финальный проект Яндекс Практикум

## Первый запуск

Эти инструкции будут охватывать информацию об использовании контейнера Docker

### Предпосылки

Для запуска этого контейнера вам понадобится установленный Docker:

* [Windows](https://docs.docker.com/windows/started)
* [Linux](https://docs.docker.com/linux/started/)

### Команда для запуска

Нужно пересобрать контейнеры и после запустить

```shell
docker-compose up -d --build
```

Комнады миграции даных в БД

```shell
docker-compose exec web python manage.py makemigrations api
docker-compose exec web python manage.py migrate --noinput
```

Команда для создания учетной записи суперпользователя

```shell
docker-compose exec web python manage.py createsuperuser
```

Команда для сбора статических фалов

```shell
docker-compose exec web python manage.py collectstatic --no-input
```

#### Используемые переменные

* `DB_NAME` - имя базы данных
* `POSTGRES_USER` - логин для подключения к базе данных
* `POSTGRES_PASSWORD` - пароль для подключения к БД (установите свой)
* `DB_HOST` - название сервиса (контейнера)
* `DB_PORT` - порт для подключения к БД

## Автор

* **Егоров Максим**

## DockerHub

Проект доступен по [ссылке](http://217.28.229.247/api/v1)

[![CI](https://github.com/n18qpc/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master)](https://github.com/n18qpc/yamdb_final/actions/workflows/yamdb_workflow.yml)
