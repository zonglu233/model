# _*_ coding:utf-8 _*_

interval = 45
daymins = 1440

graph = []
result = []


def un_lock(puck, gate):
    if puck['arrive_point'] >= gate['next_point']:
        return True
    return False


# 建立G(V,E)图
def create_matrix(pucks):
    n = len(pucks)  # n个顶点
    matrix = [([0] * n) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            # print("比较", pucks[i]['transfer_id'], pucks[j]['transfer_id'])
            body = pucks[i]['body_type'] != pucks[j]['body_type']
            time1 = (pucks[i]['leave_point'] + 45 > pucks[j]['arrive_point']) and (
                        pucks[i]['leave_point'] + 45 < pucks[j]['leave_point'])
            time2 = (pucks[i]['arrive_point'] > pucks[j]['arrive_point']) and (
                        pucks[i]['arrive_point'] < pucks[j]['leave_point'] + 45)
            time3 = (pucks[i]['arrive_point'] > pucks[j]['arrive_point']) and (
                        pucks[i]['leave_point'] + 45 < pucks[j]['leave_point'])
            time4 = (pucks[i]['leave_point'] + 45 < pucks[j]['leave_point']) and (
                        pucks[i]['arrive_point'] > pucks[j]['arrive_point'])
            if body or time1 or time2 or time3 or time4:
                # print("=================================")
                # print(pucks[i]['transfer_id'], pucks[i]['body_type'], pucks[i]['arrive_point'], pucks[i]['leave_point'])
                # print(pucks[j]['transfer_id'], pucks[j]['body_type'], pucks[j]['arrive_point'], pucks[j]['leave_point'])
                matrix[i][j] = 1
                matrix[j][i] = 1
            j = j + 1
        i = i + 1
    return matrix


# 看看登机口是否可用
def is_match(puck, gate):
    if puck['arrive_point'] >= gate['next_point']:
        if puck['body_type'] == gate['body_type']:
            if puck['arrive_type'] == gate['arrive_type'] or gate['arrive_type'] == 'A':
                if puck['leave_type'] == gate['leave_type'] or gate['leave_type'] == 'A':
                    return True
    return False


def is_confict(i, j):
    flag = True
    # 看当前航班
    iconficts = graph[i]    # 与航班i冲突的所有航班
    jpucks = result[j]      # 结果集中登机口j目前的航班
    for k in range(len(iconficts)):
        # 判断当前i航班与k航班在同一登机口是否冲突
        if iconficts[k] == 1:
            # 冲突，判断k航班是否在该登机口
            if jpucks[k] == 1:
                flag = False
                break
    return flag


def find_bg_max(puck, gates):
    index = -1
    for i in range(len(gates)):
        flag = is_match(puck, gates[i])
        if flag:
            if i == 1:
                index = i
            elif gates[i]['rest_time'] > gates[index]['rest_time']:
                index = i
    return index


def init_generation(pucks, gates):
    num_gate = len(gates)
    num_puck = len(pucks)

    AVE = interval * 2

    pucks.sort(key=lambda k: (k['cost_time']))
    # for item in pucks:
    #     print(item['cost_time'])

    gates.sort(key=lambda k: (k['arrive_type'], k['leave_type']), reverse=True)    # 按照到达顺序排序

    for item in gates:
        print(item['arrive_type'], item['leave_type'])

    global graph  # 冲突集合
    graph = create_matrix(pucks)

    global result
    result = [([0] * num_puck) for i in range(num_gate)]  # 结果集

    # 读取航班信息
    NG = gates  # 空闲登机口集合
    BG = []  # 禁忌登机口集合

    # 对每一个航班进行分配停机位
    for i in range(num_gate):
        # 先自然解禁BG中部分空闲机位
        if len(BG) > 0:
            unlocklist = []
            for k in range(len(BG)):
                if BG[k]['rest_time'] > AVE:
                    free = un_lock(pucks[i], BG[k])
                    if free:
                        unlocklist.append(k)
            if len(unlocklist):
                unlocklist.sort(reverse=True)
                for item in unlocklist:
                    NG.append(BG[item])
                    del BG[item]

        flag = True
        for j in range(num_gate):
            # 判断是否冲突
            noconfict = is_confict(i, j)
            if noconfict:
                matched = is_match(pucks[i], gates[j])
                if matched:
                    flag = False
                    result[j][i] = 1
                    # 计算登机口j的rest_time
                    NG[j]['rest_time'] = NG[j]['rest_time'] - pucks[i]['cost_time'] - 45
                    # 移到禁忌表中
                    BG.append(NG[j])
                    del NG[j]
                    break

        # 没有找到，则从BG中找
        if flag:
            # 如果没有找到，则去BG中根据 rest_time 进行查找
            bg_index = find_bg_max(pucks[i], BG)
            if bg_index >= 0:
                index = -1
                for j in range(len(range)):
                    if gates[j]['gate_id'] == BG[bg_index]['gate_id']:
                        index = j
                        break
                if index >= 0:
                    BG[bg_index]['rest_time'] = BG[bg_index]['rest_time'] - pucks[i]['cost_time'] - 45

    for i in range(len(graph)):
        print(pucks[i]['transfer_id'], "冲突", graph[i])

    total = 0
    for j in range(len(result)):
        item = result[j]
        for i in range(len(item)):
            if result[j][i] == 1:
                total = total + 1
                print(pucks[i]['transfer_id'], "--", gates[j]['gate_id'])

    print("共分配飞机：", total)
    return
