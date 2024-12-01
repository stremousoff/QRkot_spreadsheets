from typing import Optional

# Константы моделей и схем
MAX_LENGTH_NAME = 100
MIN_LENGTH_NAME = 1
INVEST_AMOUNT_DEFAULT = 0


# Константы настроек
class ConfigConstants:
    APP_TITLE = "Кошачий благотворительный фонд"
    APP_DESCRIPTION = "Сервис для поддержки котиков!"
    APP_VERSION = "0.1.0"
    DATABASE_URL = "sqlite+aiosqlite:///./fastapi.db"
    AUTH_BACKEND_NAME = "jwt"
    SECRET = "secret"


# Литералы ошибок валидации
class ValidationError:
    CHARITY_PROJECT_EXISTS = "Проект с таким именем уже существует!"
    CHARITY_PROJECT_BY_ID_NOT_FOUND = "Объект с айди с номером {} не найден."
    CHARITY_FULL_AMOUNT_ERROR = (
        "Нельзя установить значение full_amount меньше уже вложенной суммы."
    )
    DONT_DELETE_PROJECT_IF_INVEST_EXIST = (
        "В проект были внесены средства, не подлежит удалению!"
    )
    DONT_CHANGE_PROJECT_IF_INVEST_EXIST = (
        "В проект были внесены средства, не подлежит изменению!"
    )
    NAME_REQUIRED = "Поле name обязательно для заполнения."
    EXCEEDED_ROWS_AMOUNT = ("Превышено максимальное({}) количество строк в "
                            "таблице! Требуется записать {}")
    EXCEEDED_COLUMNS_AMOUNT = ("Превышено максимальное({}) количество столбцов"
                               " в таблице! Требуется записать {}")


# Литералы ошибок регистрации пользователя
class UserMessages:
    PASSWORD_ERROR = "Длина пароля должна быть не менее 8 символов!"
    PASSWORD_NOT_CONTAIN_EMAIL = "Пароль не должен содержать e-mail!"
    USER_SUCCESSFULLY_REGISTERED = "Пользователь {} зарегистрирован."


# Константы Google_api:
FORMAT_SPREADSHEET_TIME = "%Y/%m/%d %H:%M:%S"
GOOGLE_SPREADSHEET_ROWS_LIMIT = 1000000000
GOOGLE_SPREADSHEET_COLUMNS_LIMIT = 18278


SPREADSHEET_HEADER = [
    ["Отчёт от", ""],
    ["Топ проектов по скорости закрытия"],
    ["Название проекта", "Время сбора", "Описание"],
]

SPREADSHEET_BODY = dict(
    properties=dict(
        locale="ru_RU",
    ),
    sheets=[
        dict(
            properties=dict(
                sheetType="GRID",
                sheetId=0,
                title="Лист1",
                gridProperties=dict(),
            )
        )
    ],
)
