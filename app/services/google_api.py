from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

FORMAT = "%Y/%m/%d %H:%M:%S"
ROW_COUNT = 100
COLUMN_COUNT = 100
SPREADSHEET_TITLE = "Отчет на {date}"


def generate_spreadsheet_body(date: str) -> dict:
    """Генерирует тело запроса для создания таблицы."""
    return {
        "properties": {
            "title": SPREADSHEET_TITLE.format(date=date),
            "locale": "ru_RU",
        },
        "sheets": [{
            "properties": {
                "sheetType": "GRID",
                "sheetId": 0,
                "title": "Лист1",
                "gridProperties": {
                    "rowCount": ROW_COUNT,
                    "columnCount": COLUMN_COUNT,
                }
            }
        }]
    }


TABLE_HEADER = [
    ["Отчет от", None],
    ["Топ проектов по скорости закрытия"],
    ["Название проекта", "Время сбора", "Описание"]
]


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body=None
) -> str:
    """Создает новую таблицу в Google Sheets."""
    if spreadsheet_body is None:
        date_now = datetime.now().strftime(FORMAT)
        spreadsheet_body = generate_spreadsheet_body(date_now)
    service = await wrapper_services.discover("sheets", "v4")
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response["spreadsheetId"]


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """Выдает доступ пользователю к созданной таблице."""
    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email
    }
    service = await wrapper_services.discover("drive", "v3")
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    """Обновляет данные в таблице Google Sheets."""
    service = await wrapper_services.discover("sheets", "v4")
    date_now = datetime.now().strftime(FORMAT)
    table_header = deepcopy(TABLE_HEADER)
    table_header[0][1] = date_now

    table_values = [
        *table_header,
        *[
            [
                attr.name,
                str(duration),
                attr.description
            ]
            for attr in projects
            if (duration := attr.close_date - attr.create_date)
        ],
    ]

    rows = len(table_values)
    cols = max(map(len, table_values))

    if rows > ROW_COUNT or cols > COLUMN_COUNT:
        raise ValueError(
            f"Превышены габариты таблицы. "
            f"Сформировано строк {rows}. Допустимо {ROW_COUNT}. "
            f"Сформировано столбцов {cols}. Допустимо {COLUMN_COUNT}. "
        )

    update_body = {
        "majorDimension": "ROWS",
        "values": table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f"R1C1:R{rows}C{cols}",
            valueInputOption="USER_ENTERED",
            json=update_body
        )
    )
