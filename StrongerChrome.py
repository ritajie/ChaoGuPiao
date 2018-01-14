"""chrome"""
from selenium import webdriver

def StrongerChrome(i):
    """新建chrome：不加载图片、设置位置"""
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome = webdriver.Chrome(chrome_options=chrome_options)
    chrome.set_window_position(800, i*100)
    chrome.set_window_size(800, 150)
    return chrome