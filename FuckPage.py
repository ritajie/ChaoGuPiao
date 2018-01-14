"""从页面中提取数据"""
import re
import json


def get_infor_from_jsonpage(chrome):
    """从json页面中提取数据"""
    json_str0 = chrome.find_element_by_xpath('/html/body/pre').text
    json_str = (re.match(".*?\((.*}})\)", json_str0).group(1))
    thejson = json.loads(json_str)["items"]
    chengjiaoliang = thejson["13"]
    zhenfu = thejson['526792'] + "%"
    huanshou = thejson["1968584"] + "%"
    shiyinglv = thejson["2034120"]

    #把成交量换成单位为亿或万
    chengjiaoliang_float = float(chengjiaoliang)
    if chengjiaoliang_float > 100000000:
        chengjiaoliang = str(round(chengjiaoliang_float/100000000, 2)) + "亿"
    else:
        chengjiaoliang = str(round(chengjiaoliang_float/10000, 2)) + "万"

    ans = {}
    ans["成交量"] = chengjiaoliang
    ans["振幅"] = zhenfu
    ans["换手"] = huanshou
    ans["市盈率"] = shiyinglv

    return ans


def get_infor_from_nomalpage(chrome):
    """从普通界面中提取信息"""
    frame = chrome.find_element_by_xpath('//*[@id="in_squote"]/div/div/iframe')
    chrome.switch_to_frame(frame)
    chengjiaoliang = chrome.find_element_by_xpath('//*[@id="tamount"]').text
    zhenfu = chrome.find_element_by_xpath('//*[@id="trange"]').text
    huanshou = chrome.find_element_by_xpath('//*[@id="tchange"]').text
    shiyinglv = chrome.find_element_by_xpath('//*[@id="fvaluep"]').text

    ans = {}
    ans["成交量"] = chengjiaoliang
    ans["振幅"] = zhenfu
    ans["换手"] = huanshou
    ans["市盈率"] = shiyinglv
    return ans