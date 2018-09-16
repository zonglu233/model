# _*_ coding:utf-8 _*_

import xlrd
import datetime

wide_body = ["332", "333", "33E", "33H", "33L", "773"]
narrow_body = ["319", "320", "321", "323", "325", "738", "73A", "73E", "73H", "73L"]

workbook = xlrd.open_workbook("./InputData.xlsx")

def getPucks():

    pucks_sheet = workbook.sheet_by_name('Pucks')
    prows = pucks_sheet.nrows - 1
    start = datetime.datetime.strptime("2018-01-20 0:0", "%Y-%m-%d %H:%M")
    end = datetime.datetime.strptime("2018-01-21 0:0", "%Y-%m-%d %H:%M")

    pucks = []
    for i in range(1, prows):
        arrive = datetime.datetime.strptime(pucks_sheet.cell(i, 12).value, "%Y-%m-%d %H:%M")
        leave = datetime.datetime.strptime(pucks_sheet.cell(i, 13).value, "%Y-%m-%d %H:%M")

        # 查找20号的航班线路
        if leave > start and arrive < end:
            transfer_id = pucks_sheet.cell(i, 0).value
            arrive_point = int((start - arrive).seconds / 60)
            leave_point = int((leave - start).seconds / 60)
            if arrive < start:
                arrive_point = -arrive_point
                cost_time = arrive_point
            else:
                cost_time = leave_point - arrive_point
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
            transfer = {
                "transfer_id": transfer_id,
                "arrive_point": arrive_point,
                "leave_point": leave_point,
                "body_type": body_type,
                "arrive_line": arrive_line,
                "arrive_type": arrive_type,
                "leave_line": leave_line,
                "leave_type": leave_type,
                "cost_time": cost_time
            }
            pucks.append(transfer)
    return pucks


def getGates():
    gates_sheet = workbook.sheet_by_name('Gates')
    grows = gates_sheet.nrows - 1
    gates = []
    for i in range(1, grows):
        gate_id = gates_sheet.cell(i, 0).value
        gate_hall = gates_sheet.cell(i, 1).value
        area_str = gates_sheet.cell(i, 2).value
        if gate_hall == "T" and area_str == "North":
            gate_area = 0
        elif gate_hall == "T" and area_str == "Center":
            gate_area = 1
        elif gate_hall == "T" and area_str == "South":
            gate_area = 2
        elif gate_hall == "S" and area_str == "North":
            gate_area = 3
        elif gate_hall == "S" and area_str == "Center":
            gate_area = 4
        elif gate_hall == "S" and area_str == "South":
            gate_area = 5
        elif gate_hall == "S" and area_str == "East":
            gate_area = 6

        arrive_type = gates_sheet.cell(i, 3).value
        if len(arrive_type) > 1:
            arrive_type = "A"

        leave_type = gates_sheet.cell(i, 4).value
        if len(leave_type) > 1:
            leave_type = "A"

        body_type = gates_sheet.cell(i, 5).value

        gate = {
            "gate_id": gate_id,
            "gate_hall": gate_hall,
            "gate_area": gate_area,
            "arrive_type": arrive_type,
            "leave_type": leave_type,
            "body_type": body_type
        }
        gates.append(gate)
    return gates


