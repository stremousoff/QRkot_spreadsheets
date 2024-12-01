from datetime import datetime
from aiogoogle import Aiogoogle
from app.core.config import settings
from app.core.constans import FORMAT_SPREADSHEET_TIME, SPREADSHEET_TEMPLATE


def get_spreadsheet_template(
    template_type: str, _datetime: str, rows: int = None, columns: int = None
) -> dict:
    template = SPREADSHEET_TEMPLATE[template_type].copy()
    if template_type == "header":
        template[0][1] = _datetime
        return template
    template["properties"][
        "title"
    ] = f"Все закрытые сборы на {_datetime} время"
    template["sheets"][0]["properties"]["gridProperties"]["rowCount"] = rows
    template["sheets"][0]["properties"]["gridProperties"][
        "columnCount"
    ] = columns
    return template


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
    projects: list,
) -> tuple[str, str]:
    service = await wrapper_services.discover("sheets", "v4")
    num_rows = len(projects) + len(SPREADSHEET_TEMPLATE["header"])
    num_columns = max(map(len, SPREADSHEET_TEMPLATE["header"]))
    spreadsheet_body = get_spreadsheet_template(
        "body",
        datetime.now().strftime(FORMAT_SPREADSHEET_TIME),
        rows=num_rows,
        columns=num_columns,
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
    table_values = [
        *get_spreadsheet_template(
            "header", datetime.now().strftime(FORMAT_SPREADSHEET_TIME)
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
