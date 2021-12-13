# ScholarOne-manuscript-checker
Periodically check the manuscript state in the scholar one system and send email when finding a new state.

## Parameters need modification

* def send_email(msg):
  - mail_host="smtp.qq.com"  #设置服务器
	- mail_user="xxxxx@qq.com"    #用户名
	- mail_pass="pas"   #口令,qq邮箱使用授权码
	- receivers = ['xxx@gg.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

* def print_test(status):
  - b.visit('https://mc.manuscriptcentral.com/terg/') #此处设置scholar one对应期刊的网址
  - b.fill('USERID', 'Your scholar one userID') #此处设置你的scholar one账号邮箱
  - b.fill('PASSWORD','******') # 此处设置你的scholar one账号密码
  - table = soup.find("span", attrs={"class": "pagecontents"}) #此处需要依据scholar one中网页元素进行设置，用于定位页面元素。默认的可能有用

* interval = 3600       #此处设置间隔时间


## How to use
python scholarone_status_checker_new.py
