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


# Константы Google_api:
FORMAT_SPREADSHEET_TIME = "%Y/%m/%d %H:%M:%S"
GOOGLE_SPREADSHEET_CELL_LIMIT = 10_000_000
GOOGLE_SPREADSHEET_COLUMNS_LIMIT = 18_278
GOOGLE_SPREADSHEET_ROWS_LIMIT = 200_000


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
    EXCEEDED_CELL_AMOUNT = (
        f"Превышено максимальное число ячеек {{}} * {{}} > "
        f"{GOOGLE_SPREADSHEET_CELL_LIMIT}!"
    )
    EXCEEDED_COLUMN_AMOUNT = (
        f"Превышено максимальное число колонок {{}} > "
        f"{GOOGLE_SPREADSHEET_COLUMNS_LIMIT}!"
    )
    EXCEEDED_ROW_AMOUNT = (
        f"Превышено максимальное число строк {{}} > "
        f"{GOOGLE_SPREADSHEET_ROWS_LIMIT}!"
    )


# Литералы ошибок Google_api
class GoogleApiError:
    SPREADSHEET_CREATE_ERROR = "Произошла ошибка при создании таблицы: {}"


# Литералы ошибок регистрации пользователя
class UserMessages:
    PASSWORD_ERROR = "Длина пароля должна быть не менее 8 символов!"
    PASSWORD_NOT_CONTAIN_EMAIL = "Пароль не должен содержать e-mail!"
    USER_SUCCESSFULLY_REGISTERED = "Пользователь {} зарегистрирован."


# Заготовка для хедера таблицы
SPREADSHEET_HEADER = [
    ["Отчёт от", ""],
    ["Топ проектов по скорости закрытия"],
    ["Название проекта", "Время сбора", "Описание"],
]

# Заготовка для тела таблицы
SPREADSHEET_BODY = dict(
    properties=dict(
        title="",
        locale="ru_RU",
    ),
    sheets=[
        dict(
            properties=dict(
                sheetType="GRID",
                sheetId=0,
                title="Лист1",
                gridProperties=dict(
                    rowCount=0,
                    columnCount=0,
                ),
            )
        )
    ],
)
