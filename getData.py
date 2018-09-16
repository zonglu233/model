# _*_ coding:utf-8 _*_

import xlrd
import datetime

wide_body = ["332", "333", "33E", "33H", "33L", "773"]
narrow_body = ["319", "320", "321", "323", "325", "738", "73A", "73E", "73H", "73L"]


def getPucks():
    pucks = []
    workbook = xlrd.open_workbook("./InputData.xlsx")
    pucks_sheet = workbook.sheet_by_name('Pucks')
    prows = pucks_sheet.nrows - 1
    start = datetime.datetime.strptime("2018-01-20 0:0", "%Y-%m-%d %H:%M")
    end = datetime.datetime.strptime("2018-01-21 0:0", "%Y-%m-%d %H:%M")
    print(start, end)

    for i in range(1, prows):
        arrive = datetime.datetime.strptime(pucks_sheet.cell(i, 12).value, "%Y-%m-%d %H:%M")
        leave = datetime.datetime.strptime(pucks_sheet.cell(i, 13).value, "%Y-%m-%d %H:%M")

        # 查找20号的航班线路
        if leave > start and arrive < end:
            transfer_id = pucks_sheet.cell(i, 0).value
            point1 = int((start - arrive).seconds / 60)
            if arrive < start:
                point1 = -point1
            point2 = int((leave - start).seconds / 60)
            arrive_line = pucks_sheet.cell(i, 3).value
            arrive_type = pucks_sheet.cell(i, 4).value
            fly_type = pucks_sheet.cell(i, 5).value
            fly_ctype = pucks_sheet.cell(i, 5).ctype
            if fly_ctype == 2:
                fly_type = str(int(fly_type))
            body_type = ""
            if fly_type in wide_body:
                body_type = "W"
            if fly_type in narrow_body:
                body_type = "N"
            leave_line = pucks_sheet.cell(i, 8).value
            leave_type = pucks_sheet.cell(i, 9).value
            transfer = [transfer_id, point1, point2, body_type, arrive_line, arrive_type, leave_line, leave_type]
            pucks.append(transfer)
    return pucks

