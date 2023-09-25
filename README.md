# test_case_pronin_team

<details>
<summary><b>ЗАДАНИЕ:</b></summary>

tbf

</details>

## Запуск

1. Клонировать репозиторий

    ```bash
    git clone <ссылка с git-hub>
    ```

2. Перейти в папку /test_case_pronin_team

    ```bash
    cd test_case_pronin_team/
    ```

3. Создать файл .env по образцу .env.example из репозитория.  
   **Для упрощения тестового запуска рабочий .env я оставил в репозитории. После сдачи тестового задания - файл будет удалён.**

4. Поднять контейнеры в фоновом режиме

    ```bash
    docker compose up -d
    ```

5. Админка доступна по адресу <http://127.0.0.1:8000/admin/>. Чтобы воспользоваться ей - необходимо создать суперпользователя локально выполнив команду и введя свои данные.

    ```bash
    docker compose exec backend python manage.py createsuperuser
    ```

6. Чтобы прекратить работу контейнеров воспользуйтесь командой

    ```bash
    docker compose down
    ```

    Если хотите прекратить работу контейнеров с удалением томов данных, то дополните команду флагом -v

    ```bash
    docker compose down -v
    ```

## Доступные ручки

1. Загрузка нового csv-файла для обработки

    ```text
    http://127.0.0.1:8000/api/v1/add-deals
    ```

    Предоставленный для тестирования файл разположен в директории /test_case_pronin_team/test_data  
    Тестирование отправки файла на ручку проводилось через Postman с помощью form-data формата для отправки тела запроса.

    ### Формат запроса

    ```json
    {
        "deals": some_file.csv
    }
    ```

    ### Возможные ответы

    ```json
    {
        "Status": "OK"
    }
    ```

    ```json
    {
        "Status": "error",
        "Desc": "description"
    }
    ```

2. Получение списка топ-5 покупателей со списком камней

    ```text
    http://127.0.0.1:8000/api/v1/get-top
    ```

    ### Пример ответа

    ```json
    {
        "response": [
            {
                "username": "resplendent",
                "spent_money": 451731,
                "gems": [
                    "Танзанит",
                    "Рубин",
                    "Сапфир"
                ]
            },
            {
                "username": "bellwether",
                "spent_money": 217794,
                "gems": [
                    "Петерсит",
                    "Сапфир"
                ]
            },
            {
                "username": "uvulaperfly117",
                "spent_money": 120419,
                "gems": [
                    "Танзанит",
                    "Петерсит"
                ]
            },
            {
                "username": "braggadocio",
                "spent_money": 108957,
                "gems": [
                    "Изумруд"
                ]
            },
            {
                "username": "turophile",
                "spent_money": 100132,
                "gems": [
                    "Рубин",
                    "Изумруд"
                ]
            }
        ]
    }
    ```

## Контакты

**telegram** [@Menshikov_AS](https://t.me/Menshikov_AS)  
**e-mail** <a.menshikov1989@gmail.com>
