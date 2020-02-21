from selenium import webdriver
import time
import datetime
import re
import os
from twilio.rest import Client
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome(ChromeDriverManager().install())
usernameID = "unamebean"
passwordID = "pwdbean"
url = "http://mynordstrom.com"
url1 = "https://nordstrom.okta.com"
schedule = "https://nord-wfmr-prod.jdadelivers.com/retail/portal?siteId=0425#wfmess/wfmess-myschedule////"
submitID = "SubmitButton"
employee = os.environ['employeeNumber']
password = os.environ['passwordMyNords']
employee1 = os.environ['workdayUser']
password1 = os.environ['workdayPass']
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

item_list = []

# def login(url,usernameID,passwordID,submitID):
#    driver.get(url)
#    driver.find_element_by_id(usernameID).send_keys(employee)
#    driver.find_element_by_id(passwordID).send_keys(password)
#    driver.find_element_by_id(submitID).click()

def inside(url,usernameID,passwordID,submitID):
    driver.get(url)
    driver.find_element_by_name("username").send_keys(employee1)
    driver.find_element_by_name("password").send_keys(password1)
    driver.find_element_by_id("okta-signin-submit").click()
    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://nordstrom.okta.com/home/nordstrom_myschedule_1/0oa4ozg950nKI65zT2p7/aln4oziqlozjHoMnL2p7?fromHome=true']")))
    driver.find_element_by_xpath("//a[@href='https://nordstrom.okta.com/home/nordstrom_myschedule_1/0oa4ozg950nKI65zT2p7/aln4oziqlozjHoMnL2p7?fromHome=true']").click()

def scheduleClick(url):
    # driver.find_element_by_link_text(url).click()
    driver.get(url)
    # wait = WebDriverWait(driver, 20)
    # wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@role='presentation']")))
    driver.implicitly_wait(15)
    frame = driver.find_element_by_id("jdaIFrame-1025")
    driver.switch_to.frame(frame)
    driver.implicitly_wait(15)

    # for div in driver.find_elements_by_class_name("right"):
    #     print(div.text)

    for div in driver.find_elements_by_class_name("shiftdisplay"):
        html = div.get_attribute("outerHTML")
        x = re.findall(r'(?<=>)[^<.]+(?=<)',html)
        y = re.search(r'shiftstarttime\=\"(.*?)GMT-0800', html).group(1)
        date_time_obj = datetime.datetime.strptime(y, '%a %b %d %Y %H:%M:%S ')
        item_list.append((date_time_obj.date(), x))

def check(items, key):
    # print(item_list)
    for item in items:
        if item[0] == key:
            return item[1]
        else:
            return "you don't work today"

def sendMessage(message):
    work = "Your schedule for today is " + message
    message = client.messages \
                .create(
                     body= work,
                     from_= os.environ['TWILIO_NUMBER'],
                     to= os.environ['NUMBER']
                 )

    print(message.sid)

inside(url1, usernameID, passwordID, submitID)
time.sleep(5)
scheduleClick(schedule)
work = (check(item_list, datetime.datetime.now()))
sendMessage(work)


