"""
爬取同花顺股票网的信息
2018/1/8
路小鹿
"""
import time
import threading
from aThread import aThread
import FuckExcel


def get_keys(thedict, thevalue):
    """get key from dict by id"""
    return [key for key, value in thedict.items() if value == thevalue][0]


if __name__ == '__main__':
    ans_dict = {}  # 答案
    HowmanyID_eachtime = 20  # 每次传递的id数
    name_id = FuckExcel.get_nameid()  # name id大字典
    startTime = time.time()  #开始时间
    HowmanyThreads = 2  # 线程数
    threads = []  # 装线程的盒子

    print("开始解析，一共%d个, 开始时间" % len(name_id), time.ctime())

    for i in range(HowmanyThreads):
        a_thread = threading.Thread(target=aThread, args=[i, name_id, ans_dict])
        threads.append(a_thread)
    for i in range(HowmanyThreads):
        threads[i].start()
    for i in range(HowmanyThreads):
        threads[i].join()

    #保存结果到excel
    FuckExcel.save_in_excel(ans_dict)

    print("解析结束，结束时间%s" % time.ctime())