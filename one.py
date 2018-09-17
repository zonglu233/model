# coding:utf-8
from getData import getPucks, getGates

if __name__ == "__main__":

    pucks = getPucks()
    gates = getGates()

    # 生成无向图

    # 1.建立G(V,E)图
    n = len(pucks)  # n个顶点

    matrix = [([0] * n) for i in range(n)]

    for i in range(n):
        for j in range(i, n):
            body_type = pucks[i]['body_type'] == pucks[j]['body_type']
            arrive_type = pucks[i]['arrive_type'] == pucks[j]['arrive_type']
            leave_type = pucks[i]['leave_type'] == pucks[j]['leave_type']
            front = pucks[i]['arrive_point'] > pucks[j]['leave_point'] + 45
            back = pucks[i]['leave_point'] + 45 < pucks[j]['arrive_point']
            if body_type and arrive_type and leave_type and (front or back):
                matrix[i][j] = 1
                print("=============")
                print(pucks[i], pucks[j])
    for item in matrix:
        print(item)