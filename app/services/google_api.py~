import copy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constans import (
    FORMAT_SPREADSHEET_TIME,
    GOOGLE_SPREADSHEET_ROWS_LIMIT,
    GOOGLE_SPREADSHEET_COLUMNS_LIMIT,
    ValidationError,
    SPREADSHEET_HEADER,
    SPREADSHEET_BODY
)
from app.core.exceptions import MaxColumnsLimit, MaxRowsLimit


def get_spreadsheet_header(_datetime: str) -> list:
    header = copy.deepcopy(SPREADSHEET_HEADER)
    header[0][1] = _datetime
    return header


def get_spreadsheet_body(_datetime: str, rows: int, columns: int) -> dict:
    body = copy.deepcopy(SPREADSHEET_BODY)
    body["properties"]["title"] = f"Все закрытые сборы на {_datetime} время"
    grid_properties = body["sheets"][0]["properties"]["gridProperties"]
    grid_properties["rowCount"], grid_properties["columnCount"] = rows, columns
    return body


async def spreadsheets_create(
    wrapper_service: Aiogoogle,
    projects: list,
) -> tuple[str, str]:
    table_values = [
        *get_spreadsheet_header(
            datetime.now().strftime(FORMAT_SPREADSHEET_TIME)),
        *[list(map(str, [title, duration_period, description])) for
          title, duration_period, description in projects],
    ]
    rows, columns = len(table_values), max(map(len, table_values))
    if rows > GOOGLE_SPREADSHEET_ROWS_LIMIT:
        raise MaxRowsLimit(
            ValidationError.EXCEEDED_ROWS_AMOUNT.format(rows)
        )
    if columns > GOOGLE_SPREADSHEET_COLUMNS_LIMIT:
        raise MaxColumnsLimit(
            ValidationError.EXCEEDED_COLUMNS_AMOUNT.format(columns)
        )
    service = await wrapper_service.discover("sheets", "v4")
    spreadsheet_body = get_spreadsheet_body(
        datetime.now().strftime(FORMAT_SPREADSHEET_TIME),
        rows=rows,
        columns=columns
    )
    response = await wrapper_service.as_service_account(
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
    table_values = [
        *get_spreadsheet_header(
            datetime.now().strftime(FORMAT_SPREADSHEET_TIME)
        ),
        *[
            list(map(str, [title, duration_period, description]))
            for title, duration_period, description in projects
        ],
    ]
    update_body = {"majorDimension": "ROWS", "values": table_values}
    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f"R1C1:R{len(table_values)}C{max(map(len, table_values))}",
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
