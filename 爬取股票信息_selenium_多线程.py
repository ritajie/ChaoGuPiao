from selenium import webdriver
import time
import xlwt
import threading

num = 0
def getinformation(chrome, id):
    url = "http://stockpage.10jqka.com.cn/" + str(id) + "/"
    chrome.get(url)

    name = chrome.find_element_by_xpath('//*[@id="in_squote"]/div/h1/a[1]/strong').text
    chrome.switch_to.frame('ifm')
    chengjiaoliang = chrome.find_element_by_xpath('//*[@id="tamount"]').text
    zhenfu = chrome.find_element_by_xpath('//*[@id="trange"]').text
    huanshou = chrome.find_element_by_xpath('//*[@id="tchange"]').text
    shiyinglv = chrome.find_element_by_xpath('//*[@id="fvaluep"]').text

    return name, id, chengjiaoliang, zhenfu, huanshou, shiyinglv


def writeline(sheet, line, name="名称",id="代码", chengjiaoliang="成交量", zhenfu="振幅",
              huanshou="换手", shiyinglv="市盈率（动）"):
    arr = [name, id, chengjiaoliang, zhenfu,
           huanshou, shiyinglv]
    for lie in range(6):
        sheet.write(line, lie, arr[lie])

def main(file, eachline, hang):
    global num
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome = webdriver.Chrome(chrome_options=chrome_options)
    chrome.set_window_position(800, 0)
    # 初始化excell


    # 开始读txt文件
    time.sleep(1)
    eachline = file.readline()
    while eachline:
        arr = eachline.split("\t")
        name = arr[1].strip()
        id = arr[0].strip()
        if len(id)*len(name) == 0:
            eachline = file.readline()
            continue
        try:
            name, id, chengjiaoliang, zhenfu, huanshou, shiyinglv = getinformation(chrome, id)
            print(str(num) + "\t" + name + "\t" + chengjiaoliang + "\t" + zhenfu + "\t" + huanshou + "\t" + shiyinglv + "\t" + time.asctime(time.localtime(time.time())))
            writeline(sheet, hang, name, id, chengjiaoliang, zhenfu, huanshou, shiyinglv)
            hang += 1
        except :
            pass
            #print(num, name, "error id = ", id)

        num += 1
        eachline = file.readline()

    chrome.close()


if __name__ == '__main__':
    threads = []
    #配置目标文件excel
    ansxls = xlwt.Workbook(encoding='ascii')
    sheet = ansxls.add_sheet("2018.1.1深交所A股代码")
    hang = 0
    writeline(sheet, 0)
    hang += 1
    file = open(R"C:\Users\15517\Desktop\深交所上市.txt", "r")
    eachline = "ha"

    HowmanyThreads = 10
    for i in range(HowmanyThreads):
        a_thread = threading.Thread(target=main, args=(file, eachline, hang))
        threads.append(a_thread)
    for i in range(HowmanyThreads):
        threads[i].start()
    for i in range(HowmanyThreads):
        threads[i].join()

    print("\ngone!")

    file.close()
    ansxls.save(ansxls.save(R"C:\Users\15517\Desktop\2018.1.1深交所.xls"))