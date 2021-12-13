#-- coding:UTF-8 --
import os
import time
from subprocess import check_output
from bs4 import BeautifulSoup
from splinter import Browser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

def print_ts(message):
    print( "[%s] %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))
def run(interval, command):
    print_ts("-"*100)
    print_ts("Command %s"%command)
    print_ts("Starting every %s seconds."%interval)
    print_ts("-"*100)
    current_status = "NULL"
    while True:
        try:
            # sleep for the remaining seconds of interval
            time_remaining = interval-time.time()%interval
            print_ts("Sleeping until %s (%s seconds)..."%((time.ctime(time.time() + time_remaining)), time_remaining))
            time.sleep(time_remaining)
            print_ts("Starting command.")
            # execute the command
            status = os.system(command)
            current_status = print_test(current_status)
            print_ts("-"*100)
        except Exception:
            print('error')

def send_email(msg):
	# 第三方 SMTP 服务
	mail_host="smtp.qq.com"  #设置服务器
	mail_user="xxxxx@qq.com"    #用户名
	mail_pass="pas"   #口令,qq邮箱使用授权码
	 
	sender = mail_user #发邮件的邮箱，使用上一步中设置的
	receivers = ['xxx@gg.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
	 
	message = MIMEText('There has been a new status change: \n \n \n' + msg + '\n \n Check it in https://mc.manuscriptcentral.com/terg/', 'plain', 'utf-8') #修改为目标网页地址
	message['From'] = Header("Status Monitoring Kit", 'utf-8')
	message['To'] =  Header("userName", 'utf-8')
	
	subject = 'Manuscript Status'
	message['Subject'] = Header(subject, 'utf-8')
	 
	 
	try:
	    smtpObj = smtplib.SMTP() 
	    smtpObj.connect(mail_host, 587)    # 587 为 SMTP 端口号，
	    smtpObj.login(mail_user,mail_pass)  
	    smtpObj.sendmail(sender, receivers, message.as_string())
	    print("邮件发送成功")
	except smtplib.SMTPException:
	    print("Error: 无法发送邮件")

def print_test(status):

	wait_delay = 1
	previous_manuscript_status=status

	print('Previous status of manuscript was : ' + previous_manuscript_status)
	time.sleep(wait_delay)

	b = Browser('chrome', headless=True)
	time.sleep(wait_delay)
	b.visit('https://mc.manuscriptcentral.com/terg/') #此处设置scholar one对应期刊的网址
	time.sleep(wait_delay)
	b.fill('USERID', 'Your scholar one userID') #此处设置你的scholar one账号邮箱
	time.sleep(wait_delay)
	b.fill('PASSWORD','******') # 此处设置你的scholar one账号密码
	time.sleep(wait_delay)
	b.click_link_by_id('logInButton')
	time.sleep(wait_delay)
	b.click_link_by_partial_href("AUTHOR")
	time.sleep(wait_delay)
	html_obj = b.html
	soup = BeautifulSoup(html_obj,"lxml")
	#  soup = BeautifulSoup(html_obj)
	# table = soup.find("table", attrs={"class":"table table-striped rt cf"})
	table = soup.find("span", attrs={"class": "pagecontents"}) #此处需要依据scholar one中网页元素进行设置，用于定位页面元素。默认的可能有用
	print(table.string)
	# row = table.tbody.findAll('tr')[1]
	# first_column_html = str(row.findAll('td')[1].contents[0])
	current_manuscript_status = table.string
	# current_manuscript_status = BeautifulSoup(first_column_html,"lxml").text
	# current_manuscript_status = 'demo'
	# print current_status_msg
	time.sleep(wait_delay)
	b.quit()

	if current_manuscript_status == previous_manuscript_status:
		print('Your manucsript status remains unchanged ...')
		print('Please check back later \n')
	else:
		print("There has been a new status change... Sending updated paper status through email")
		send_email(current_manuscript_status)
		previous_manuscript_status = current_manuscript_status

	return current_manuscript_status



if __name__=="__main__":
    interval = 3600       #此处设置间隔时间
    command = r"ls"
    run(interval, command)

