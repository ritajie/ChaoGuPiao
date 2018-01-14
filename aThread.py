"""线程"""
import StrongerChrome
import FuckPage


def getsmalldict(name_id, HowmanyTab_eachtime):
    """从所有name、id键值对大字典中提取20对nameid return字典"""
    smalldict = {}
    for name in name_id:
        id = name_id[name]
        smalldict[name] = id
        if len(smalldict) == HowmanyTab_eachtime:
            break

    for name in smalldict:
        name_id.pop(name)

    return smalldict


def from_id_to_finalAns(chrome, small_dict, name_id, FinalAnsDict):
    """通过对小字典里20个id解析 获取数据填充到最终答案里"""

    # 参数列表
    # chrome 不解释
    # small_dict 装有20个name、id的小字典 供你解析
    # name_id 装有所有还没解析的name、id大字典，此处是为了让遇到403的id遣还
    # FinalAnsDict 最终答案大字典

    # 标记正在解析第几个id
    num = 0
    # 成功解析的id数
    HowmanyGet = 0
    # 标记状态first_id第一次解析id、js_nomal、js_403
    flag = "first_id"
    # 开始解析每个id
    for name, id in small_dict.items():
        # 第一次解析 用普通界面打开
        if flag == "first_id":
            nomal_url = "http://stockpage.10jqka.com.cn/" + id + "/?qq-pf-to=pcqq.c2c"
            chrome.get(nomal_url)
            smallAnsDict = FuckPage.get_infor_from_nomalpage(chrome)
            # 为结果字典添加id属性
            smallAnsDict["ID"] = id
            HowmanyGet += 1
            FinalAnsDict[name] = smallAnsDict
            flag = "js_nomal"
        # 剩下的界面用json页面打开 注意取完数据后就关闭之
        elif flag == "js_nomal":
            json_url = "http://d.10jqka.com.cn/v2/realhead/hs_" + id + "/last.js"
            js = "window.open('%s')" % json_url
            # 打开新窗口
            chrome.execute_script(js)
            # 切换至新窗口
            chrome.switch_to.window(chrome.window_handles[-1])
            # 如果解析失败
            if "403 Forbidden" in chrome.page_source:
                # 将name id重新添加到name_id大原始字典
                name_id[name] = id
                # 并标记403 （此标记让之后没解析的id也别解析了
                flag = "js_403"
            # 如果解析成功
            else:
                smallAnsDict = FuckPage.get_infor_from_jsonpage(chrome)
                smallAnsDict["ID"] = id
                FinalAnsDict[name] = smallAnsDict
                HowmanyGet += 1
            # 关闭json页面
            chrome.close()
            # 回到正常页面（第一个页面）
            chrome.switch_to.window(chrome.window_handles[0])
        # 如果已经在上面标记了403
        elif flag == "js_403":
            # 也别用chrome打开了 直接扔回name_id大字典（甭担心，咱会卷土重来的！
            name_id[name] = id

    # 返回成功解析的id数
    return HowmanyGet


def isfull(thelist):
    """判断列表是否满了（10个）"""
    return len(thelist) >= 10


def myTime(Sec):
    """将整数秒数化为多少分钟多少秒字符串"""
    min = 0
    sec = 0
    if Sec > 60:
        min = Sec // 60
    sec = int(Sec) % 60
    return "%d分%d秒" % (min, sec)


def aThread(i, name_id, ans_dict):
    """单个线程"""
    # name_id 含有所有id的大字典
    # ans_dict 放解析结果的大字典

    # 新建chrome 不加载图片 位置根据线程序数i调整
    chrome = StrongerChrome.StrongerChrome(i)
    # 随便给个初始url
    chrome.get("http://baidu.com")
    # 只要大字典不为空 就一直解析
    while len(name_id) != 0:
        # 获取小字典 含有20个id
        small_dict = getsmalldict(name_id, 20)
        # 解析之 （name_id大字典是用来处理403界面 加入出现403 该id要还给name_id大字典
        HowmanyIDGet = from_id_to_finalAns(chrome, small_dict, name_id, ans_dict)

        print("%d\t %d线程搞定了：%d个 \t剩余%d" % (len(ans_dict), i, HowmanyIDGet, len(name_id)))
