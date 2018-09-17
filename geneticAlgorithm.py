# _*_ coding:utf-8 _*_
# coding:utf-8
from initGeneration import init_generation
from getData import get_pucks, get_gates

if __name__ == "__main__":
    pucks = get_pucks()
    gates = get_gates()

    # 初始化第一条染色体
    chromosomeMatrix = init_generation(pucks, gates)
    print(chromosomeMatrix)
