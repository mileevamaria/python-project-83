# Менеджер URL (Flask)

[![Actions Status](https://github.com/mileevamaria/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/mileevamaria/python-project-83/actions)
[![python-package](https://github.com/mileevamaria/python-project-83/actions/workflows/python-package.yml/badge.svg)](https://github.com/mileevamaria/python-project-83/actions/workflows/python-package.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mileevamaria_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mileevamaria_python-project-83)

https://python-project-83-whh1.onrender.com

Веб-приложение для анализа и отслеживания веб-сайтов. Позволяет добавлять URL-адреса, проверять их доступность и сохранять результаты проверок. Проект реализован на Flask и демонстрирует работу с формами, базой данных и обработкой HTTP-запросов.

### Возможности
- Добавление сайтов (URL)
- Проверка доступности сайта
- Сохранение результатов проверок
- Отображение истории проверок
- Валидация URL и обработка ошибок
- Интерфейс с использованием Bootstrap

### Стек технологий
* Python 3
* Flask
* PostgreSQL (или SQLite для разработки)
* Bootstrap 5
* Gunicorn (для деплоя)

### Установка
```shell
git clone git@github.com:mileevamaria/python-project-83.git
brew install uv
make install && psql -a -d $DATABASE_URL -f database.sql
make start
```
