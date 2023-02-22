# NER service

## Cервис с НТТP-API для распознавания именованных сущностей в текстах естественного языка

### Аннотация
Задача распознавания именованных сущностей(NER) - одна из самых популярных в сфере обработки естественного языка(NLP). 
Главная цель этой задачи - извлечение краткой полезной информации из текстов, для понимания человеком его полезности. 
Например, извлечь все названия организаций, ФИО личностей или страны из текста письма/статьи/отчета.

В рамках сервиса используется предварительно обученная [модель](https://spacy.io/models/en#en_core_web_sm), 
доступная в spacy по умолчанию. Выбор spacy для реализации NER обоснован тем, 
что функционал spacy позволяет достаточно легко подготавливать модели нейронных сетей 
для [собственных задач NLP](https://spacy.io/usage/linguistic-features#named-entities). 
Поэтому разработанный сервис можно будет применять также для задач типа NER с кастомными моделями, 
обученными под конкретный задачи.


### Реализованный функционал
1. [x] Извлечение именованных сущностей из текстов, загруженных пользователем, с помощью spacy
2. [x] Асинхронная работа сервиса;
3. [x] Авторизация через headers/cookies с использованием JWT;
4. [x] Хранение информации о пользователях, обработанных отчетах в PostgreSQL;
5. [x] Предоставление истории отчетов конкретного пользователя;
6. [x] Получение сводной статистики по извлеченным из текста именованным сущностям;
7. [x] Frontend с использованием Jinja2.


### Пример запуска
Предварительно на машине, где будет запускаться сервис, должен быть установлен 
docker(23.0.0+) и docker-compose(2.16.0+).

Далее, из корневой директории проекта выполните:
```shell
docker compose up -d --build
```
Чтобы остановить и удалить все сервисы, контейнеры и связанные образы, выполните:
```shell
docker compose down -v --rmi="all"
```




