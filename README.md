# Сервис авторизации
API для авторизации и аутентификации, основанная на JWT-токенах и RBAC подходе к управлению доступом.


## Настройка проекта
Проект использует Poetry для управления виртуальным окружениям и зависимостями.
#### Установите Poetry (не входя в виртуальное окружение)
```shell
pip3 install poetry
```

<details>
<summary><h3 style="display: inline;"> 
Как настроить проект для разработки
</h3></summary>

#### 1. Установите зависимости проекта
```shell
poetry install
```

#### 2. Используйте команды poetry для работы
https://python-poetry.org/docs/cli/

https://python-poetry.org/docs/managing-dependencies/

**Активировать виртуальное окружение:**
```shell
poetry shell
```

**Запустить команду в виртуальном окружении** (можно запускать извне окружения)
```shell
poetry run python3 auth_service/src/main.py # пример запуска команды
```

**Установить библиотеку в виртуальном окружении** (можно запускать извне окружения)
```shell
poetry add pendulum==2.0.5 # пример установки библиотеки
```
**Установить библиотеку, которая используется только в разработке** (можно запускать извне окружения)
```shell
poetry add pendulum==2.0.5 --group dev
```

#### 3. Установите pre-commit хуки
```shell
poetry run pre-commit install
```
</details>


<details>
<summary><h3 style="display: inline;"> 
Make команды
</h3></summary>

- `make tests` - запускает тесты из `./tests`
- `make lint` - проводит линтинг с помощью ruff (flake8 + isort + ...), mypy и blue (форк blake)
- `make format` - форматирует код с помощью blue
- `make build` - собирает сервис через docker-compose
- `make run` - запускает сервис через docker-compose

</details>

<details>
<summary><h3 style="display: inline;"> 
Как настроить проект для запуска
</h3></summary>

#### 1. Установите зависимости проекта
```shell
poetry install --without dev
```

#### 2. Запустите сервис
```shell
make run
```

</details>

## Авторы
[Polinavas95](https://github.com/Polinavas95)
| <tatsuchan@mail.ru>

[Barahlush](https://github.com/Barahlush) | <baraltiva@gmail.com>