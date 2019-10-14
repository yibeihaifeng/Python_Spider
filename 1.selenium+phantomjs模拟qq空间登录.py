from selenium import webdriver

import time

# 启动phantomjs无界面浏览器
browser = webdriver.Chrome()

# 打开qq空间登录界面
url = 'https://qzone.qq.com'
browser.get(url)

# 全屏截取

browser.maximize_window()
time.sleep(2)

# 确定打开了登录页面 ，保存截图
browser.save_screenshot('qq1.png')

# todo：获取登录名和密码输入框的id，使用id获取元素并在对应输入框内输入登录信息
# 切换至登录框架
browser.switch_to.frame('login_frame')
# 点击使用用户名和密码登录
# browser.find_element_by_id('switcher_plogin').click()
# browser.find_element_by_id('u').send_keys('1192535724')
# browser.find_element_by_id('p').send_keys('910402lyh')
# 保存输入用户名和密码后的截图
browser.save_screenshot('qq2.png')


# todo： 或者 也可以 直接点击头像登录
browser.find_element_by_xpath('//*[@id="qlogin_list"]/a[1]').click()
# # 保存屏幕快照
time.sleep(3)
browser.save_screenshot('qq3.png')



'''
# 注意运行时若报错：Message: 'chromedriver' executable needs to be in PATH.
需要下载谷歌浏览器版本对应的chromedriver   ：下载地址：http://npm.taobao.org/mirrors/chromedriver/ 

第一步：下载chromedriver.exe文件，将其放到谷歌浏览器可执行文件同目录
第二步：将chromedriver.exe放到Python的脚本目录下如"C:\Python27\Scripts"即可，当然放在py程序当前目录下自然可以
'''