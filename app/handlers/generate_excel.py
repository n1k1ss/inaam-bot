import xlsxwriter
from io import BytesIO
from datetime import datetime
import zoneinfo

from handlers.get_current_region import get_current_region
from inaam_bot_logger import logger
from handlers.db import db

MONTHS = {
    1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
    5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
    9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
}

async def export_to_excel(duration: str):
    try:
        current_region = await get_current_region()

        tz = zoneinfo.ZoneInfo(current_region)

        now = datetime.now(tz)
        current_month = now.month
        current_year = now.year

        if duration == "month":
            start_month = current_month
            months_count = 1

        elif duration == "quarter":
            start_month = ((current_month - 1) // 3) * 3 + 1
            months_count = 3

        elif duration == "half":
            start_month = 1 if current_month <= 6 else 7
            months_count = 6

        elif duration == "year":
            start_month = 1
            months_count = 12

        end_month = start_month + months_count - 1

        query = """
            SELECT * FROM balance_expenses
            WHERE year = $1 AND month BETWEEN $2 AND $3
            ORDER BY year, month, day
        """
        rows = await db.fetch(query, current_year, start_month, end_month)

        if not rows:
            return None

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet("Данные")

        italic_center = workbook.add_format({'italic': True, 'align': 'center', 'valign': 'vcenter'})
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
        link_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'font_color': 'blue', 'underline': 1})

        headers = ["Деятель", "День", "Месяц", "Год", "Тип", "Сумма"]
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, bold_center)
            worksheet.set_column(col_num, col_num, 20)

        for row_num, row in enumerate(rows, start=1):
            month_name = MONTHS.get(row["month"], row["month"])
            worksheet.write_url(row_num, 0, f"https://t.me/{row['doer_username']}", link_format, string=row["doer"])
            worksheet.write(row_num, 1, row["day"], italic_center)
            worksheet.write(row_num, 2, month_name, italic_center)
            worksheet.write(row_num, 3, row["year"], italic_center)
            worksheet.write(row_num, 4, f"{row['section']}", italic_center)
            worksheet.write(row_num, 5, f"{row['amount']:,}₽", italic_center)

        workbook.close()
        output.seek(0)

        return output
    except Exception as e:
        logger.exception(f"Ошибка в функции export_to_excel [generate_excel.py] [{e}]")