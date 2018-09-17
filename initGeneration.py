# _*_ coding:utf-8 _*_

interval = 45
daymins = 1440

# 看看NG集合中是否有可用登机口
def match_cg(puck, gate):
    # print(puck, gate)
    # print("===================")
    if puck['arrive_point'] >= gate['next_point']:
        if puck['body_type'] == gate['body_type']:
            if puck['arrive_type'] == gate['arrive_type'] or gate['arrive_type'] == 'A':
                if puck['leave_type'] == gate['leave_type'] or gate['leave_type'] == 'A':
                    return True
    return False


def un_lock(puck, gate):
    if puck['arrive_point'] >= gate['next_point']:
        return True
    return False


def find_bg_max(puck, gates):
    index = -1
    for i in range(len(gates)):
        flag = match_cg(puck, gates[i])
        if flag:
            if i == 1:
                index = i
            elif gates[i]['rest_time'] > gates[index]['rest_time']:
                index = i
    return index


def init_generation(pucks, gates):
    num_gate = len(gates)
    num_puck = len(pucks)
    sum_cost = 0
    # 计算平均空闲时间 AVE
    for item in pucks:
        sum_cost = sum_cost + item['cost_time']
    # print(sum_cost, num_gate)

    AVE = interval * 2

    # 读取航班信息
    NG = gates  # 空闲登机口集合
    BG = []     # 禁忌登机口集合
    for i in range(num_puck):
        # 先自然解禁BG中部分空闲机位
        if len(BG) > 0:
            unlocklist = []
            for k in range(len(BG)):
                if BG[k]['rest_time'] > AVE:
                    free = un_lock(pucks[i], BG[k])
                    if free:
                        # print(BG[k]['gate_id'], "满足解封条件")
                        unlocklist.append(k)
            if len(unlocklist):
                unlocklist.sort(reverse=True)
                for item in unlocklist:
                    NG.append(BG[item])
                    del BG[item]

        # 找满足条件的空闲机位
        flag = False
        for j in range(len(NG)):
            matched = match_cg(pucks[i], NG[j])
            # 找到了满足条件的
            if matched:
                flag = True
                pucks[i]['gate'] = NG[j]['gate_id']
                if pucks[i]['leave_point'] != daymins:
                    NG[j]['next_point'] = int(pucks[i]['leave_point'] + interval)
                else:
                    NG[j]['next_point'] = daymins
                NG[j]['rest_time'] = int(daymins - NG[j]['next_point'])
                # 移到禁忌表中
                BG.append(NG[j])
                del NG[j]
                break

        if not flag:
            # 如果没有找到，则去BG中根据 rest_time 进行查找
            bg_index = find_bg_max(pucks[i], BG)
            if bg_index >= 0:
                pucks[i]['gate'] = BG[bg_index]['gate_id']
                BG[bg_index]['next_point'] = int(pucks[i]['leave_point'] + interval)
                BG[bg_index]['rest_time'] = int(daymins - BG[bg_index]['next_point'])
                # 手动解封BG
                NG.append(BG[bg_index])
                del BG[bg_index]
    print("==========================")
    temp = 0
    fixed = 0
    for item in pucks:
        if 'gate' in item:
            # print(item['transfer_id'], " - ", item['gate'])
            fixed = fixed + 1
        else:
            # print(item['transfer_id'], " - 临时停机坪")
            temp = temp + 1

    print("固定转机个数：", fixed)
    print("临时停机坪个数：", temp)
    return
