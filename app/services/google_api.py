from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"


def get_spreadsheet_header(_datetime: str) -> list:
    return [
        ["Отчёт от", _datetime],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]


def get_spreadsheet_body(_datetime: str, rows: int, columns: int) -> dict:
    return dict(
        properties=dict(
            title=f"Все закрытые сборы на {_datetime} время",
            locale="ru_RU",
        ),
        sheets=[
            dict(
                properties=dict(
                    sheetType="GRID",
                    sheetId=0,
                    title="Лист1",
                    gridProperties=dict(rowCount=rows, columnCount=columns),
                )
            )
        ],
    )


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
    projects: list,
) -> tuple[str, str]:
    service = await wrapper_services.discover("sheets", "v4")
    spreadsheet_body = get_spreadsheet_body(
        datetime.now().strftime(FORMAT),
        rows=len(projects) + len(get_spreadsheet_header("")),
        columns=max(map(len, get_spreadsheet_header(""))),
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response["spreadsheetId"], response["spreadsheetUrl"]


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email,
    }
    service = await wrapper_services.discover("drive", "v3")
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str, wrapper_service: Aiogoogle, projects: list
) -> None:
    service = await wrapper_service.discover("sheets", "v4")
    print(projects)
    table_values = [
        *get_spreadsheet_header(datetime.now().strftime(FORMAT)),
        *[
            list(map(str, [title, duration_period, description]))
            for title, duration_period, description in projects
        ],
    ]
    update_body = {"majorDimension": "ROWS", "values": table_values}
    num_rows = len(table_values)
    num_columns = max(map(len, table_values))
    spreadsheet_body = get_spreadsheet_body(
        datetime.now().strftime(FORMAT),
        rows=num_rows,
        columns=num_columns,
    )
    num_rows_spreadsheet = spreadsheet_body["sheets"][0]["properties"][
        "gridProperties"
    ]["rowCount"]
    num_columns_spreadsheet = spreadsheet_body["sheets"][0]["properties"][
        "gridProperties"
    ]["columnCount"]
    if (
        num_rows > num_rows_spreadsheet or
            num_columns > num_columns_spreadsheet
    ):
        raise ValueError("Таблица не влезает в заготовку")

    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f"R1C1:R{num_rows}C{num_columns}",
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
