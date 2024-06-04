# Бэкенд для склада рулонов металла
Проект представляет собой бэкенд на Python для управления складом рулонов металла.

## Особенности
1. **Добавление нового рулона на склад**
    - Длина и вес обязательные параметры. 
    - Возвращает добавленный рулон при успехе.

2. **Удаление рулона с указанным ID со склада**
    - Возвращает удаленный рулон при успехе.

3. **Получение списка рулонов со склада**
    - Возможность фильтрации по одному диапазону в один момент времени (ID/вес/длина/дата добавления/дата удаления со склада).

4. **Получение статистики по рулонам за определенный период**
    - Количество добавленных рулонов.
    - Количество удаленных рулонов.
    - Средняя длина и вес рулонов на складе в этот период.
    - Максимальная и минимальная длина и вес рулонов на складе в этот период.
    - Суммарный вес рулонов на складе за период.
    - Максимальный и минимальный промежуток между добавлением и удалением рулона.
5. Получение списка рулонов с фильтрацией работает по комбинации нескольких диапазонов сразу.
6. Получение статистики по рулонам дополнительно возвращает:
    - день, когда на складе находилось минимальное и максимальное количество рулонов за указанный период;
    - день, когда суммарный вес рулонов на складе был минимальным и максимальным в указанный период.
7. Данные по рулонам хранятся в базе данных PostgreSQL.
8.  Конфигурации к подключению к БД настраиваются через файл ENV.
9.  Проект проходит flake8.
10. Обработаны стандартные кейсы ошибок (например, недоступна БД, не существует рулон при какой-то работе с ним).
11.  Отсутствие глобальных переменных
12.  Используемый стек: FastAPI, SQLAlchemy, pydantic, Alembic
