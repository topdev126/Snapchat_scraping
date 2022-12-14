from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import time
import random
import os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import urljoin
ua = UserAgent()

def type_keys(element: WebElement, text: str):
    for character in text:
        delay = random.uniform(0.1, 0.2)
        element.send_keys(character)
        time.sleep(delay)

chrome_options = ChromeOptions()
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-site-isolation-trials")
chrome_options.add_argument("--disable-application-cache")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--ignore-certificate-errors')

dPath = os.path.join(os.path.dirname(__file__),"./chromedriver")
driver = Chrome(executable_path=dPath, options=chrome_options)

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source":
        "const newProto = navigator.__proto__;"
        "delete newProto.webdriver;"
        "navigator.__proto__ = newProto;"
})


# driver.get("https://web.snapchat.com")
driver.get("https://agileway.substack.com/archive")

time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break 
##### Extract Reddit URLs #####
urls = []
soup = BeautifulSoup(driver.page_source, "html.parser")
for parent in soup.find_all(class_="post-preview-title newsletter"):
    a_tag = parent.find("a", class_="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE")
    base = "https://www.reddit.com/search/?q=covid19"
    link = a_tag.attrs['href']
    url = urljoin(base, link)
    urls.append(url)

    messagesBox = soup.find_element(By.XPATH, "//div[@aria-label='grid']")













#     from selenium.webdriver import Chrome,ChromeOptions
# from selenium.webdriver import ChromeOptions
# from selenium.webdriver.support.ui import WebDriverWait as W
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException 
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.common.keys import Keys
# import time
# import random
# import os
# from fake_useragent import UserAgent
# ua = UserAgent()

# def type_keys(element: WebElement, text: str):
#     for character in text:
#         delay = random.uniform(0.1, 0.2)
#         element.send_keys(character)
#         time.sleep(delay)

# chrome_options = ChromeOptions()
# chrome_options.add_argument("--disable-web-security")
# chrome_options.add_argument("--disable-site-isolation-trials")
# chrome_options.add_argument("--disable-application-cache")
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--start-maximized')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# chrome_options.add_argument('--ignore-certificate-errors')
# #chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"')

# #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36

# dPath = os.path.join(os.path.dirname(__file__),"./chromedriver")
# driver = Chrome(executable_path=dPath, options=chrome_options)

# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     "source":
#         "const newProto = navigator.__proto__;"
#         "delete newProto.webdriver;"
#         "navigator.__proto__ = newProto;"
# })

# def loadAllMessagesOld():
#     messagesBox = driver.find_element(By.XPATH, "//div[@aria-label='grid']")
#     time.sleep(1)

#     verical_ordinate = 100
#     for i in range(0, 140):
#         print(str(verical_ordinate))
#         driver.execute_script("arguments[0].scrollTop = arguments[1]", messagesBox, verical_ordinate)
#         verical_ordinate += 100
#         time.sleep(0.1)

# def loadAllMessages():
#     scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    
#     i = 1
#     messagesBox = driver.find_element(By.XPATH, "//div[@aria-label='grid']")
#     screen_height = driver.execute_script("return window.screen.height;", messagesBox)   # get the screen height of the web
#     # driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", messagesBox)

#     while True:
#         # scroll one screen height each time
#         driver.execute_script("arguments[0].scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i), messagesBox)  
#         # messagesBox = driver.find_element(By.XPATH, "//div[@aria-label='grid']")
#         i += 1
#         time.sleep(scroll_pause_time)
#         # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
#         # scroll_height = driver.execute_script("return document.body.scrollHeight;")  
#         scroll_height = driver.execute_script("return arguments[0].scrollHeight;", messagesBox)
#         # Break the loop when the height we need to scroll to is larger than the total scroll height
#         if (screen_height) * (i-3) > scroll_height:
#             break 

# def massMessage():
#     time.sleep(5)
#     print("Loading all messages, this can take some time..")
#     loadAllMessages()
#     #putting code to load all messages between here and the print all messages loads..



#     print("All messages have been loaded.")
#     messagesBox = driver.find_element(By.XPATH, "//div[@aria-label='grid']")
#     driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", messagesBox)
#     msgCount = driver.find_elements(By.XPATH, "//div[@role='gridcell']")
#     print(len(msgCount), " Chats found.")  



# def login():

#     try:
#         driver.get("https://web.snapchat.com")
#     except TimeoutException as e:
#         print("DEBUG: Proxy or Connection Error: " + str(e)) 
    
#     try:
#         acceptCookiesBtn = W(driver, 10).until(EC.element_to_be_clickable((By.ID, "cookiePopupAcceptEU")))
#         time.sleep(0.5)
#         acceptCookiesBtn.click()
#     except: pass

#     username = "paige420x"
#     password = "Paige1337"

#     userInputElement = W(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
#     passInputElement = W(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
#     try:
#         acceptCookiesBtn = W(driver, 10).until(EC.element_to_be_clickable((By.ID, "cookiePopupAcceptEU")))
#         time.sleep(0.5)
#         acceptCookiesBtn.click()
#     except: pass
#     time.sleep(1)
#     ActionChains(driver).move_to_element(userInputElement).click().perform()
#     type_keys(userInputElement, username)
#     time.sleep(0.3)
#     ActionChains(driver).move_to_element(passInputElement).click().perform()
#     type_keys(passInputElement, password)
#     time.sleep(0.2)

#     loginBtn = driver.find_element(By.XPATH, '//*[@id="login_form"]/div[4]/button')
#     ActionChains(driver).move_to_element(loginBtn).click().perform()

#     print("Please confirm login in app within 60 seconds.")
#     W(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
#     print("Login Success")


#     time.sleep(10)
#     ActionChains(driver).send_keys(Keys.ESCAPE).perform()

#     massMessage()
    
#     time.sleep(60)


# login()

from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import time
import random
import os
from fake_useragent import UserAgent
from itertools import chain
ua = UserAgent()

def type_keys(element: WebElement, text: str):
    for character in text:
        delay = random.uniform(0.1, 0.2)
        element.send_keys(character)
        time.sleep(delay)

chrome_options = ChromeOptions()
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-site-isolation-trials")
chrome_options.add_argument("--disable-application-cache")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--ignore-certificate-errors')
#chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"')

#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36

dPath = os.path.join(os.path.dirname(__file__),"./chromedriver")
driver = Chrome(executable_path=dPath, options=chrome_options)

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source":
        "const newProto = navigator.__proto__;"
        "delete newProto.webdriver;"
        "navigator.__proto__ = newProto;"
})

def loadAllMessagesOld():
    messagesBox = driver.find_element(By.XPATH, "//div[@aria-label='grid']")
    time.sleep(1)

    verical_ordinate = 100
    for i in range(0, 140):
        print(str(verical_ordinate))
        driver.execute_script("arguments[0].scrollTop = arguments[1]", messagesBox, verical_ordinate)
        verical_ordinate += 100
        time.sleep(0.1)

def loadAllMessages():
    scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    messagesBox = driver.find_element(By.XPATH, "//div[@aria-label='grid']")
    screen_height = driver.execute_script("return window.screen.height;", messagesBox)   # get the screen height of the web
    msgs, pastScrollHei, i = [], 0, 1
    while True:
        # scroll one screen height each time
        driver.execute_script("arguments[0].scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i), messagesBox)  
        # messagesBox = driver.find_element(By.XPATH, "//div[@aria-label='grid']")
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return arguments[0].scrollHeight;", messagesBox)
        if scroll_height != pastScrollHei:
            msgs.append(driver.find_elements(By.XPATH, "//div[@role='gridcell']"))
            pastScrollHei = scroll_height
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * (i-3) > scroll_height:
            break
    allMsgs = list(chain.from_iterable(msgs))

    return allMsgs

def massMessage():
    time.sleep(5)
    print("Loading all messages, this can take some time..")
    allMsgs= loadAllMessages()
    #putting code to load all messages between here and the print all messages loads..
    print(len(allMsgs), " Chats found.")  

def login():

    try:
        driver.get("https://web.snapchat.com")
    except TimeoutException as e:
        print("DEBUG: Proxy or Connection Error: " + str(e)) 
    
    try:
        acceptCookiesBtn = W(driver, 10).until(EC.element_to_be_clickable((By.ID, "cookiePopupAcceptEU")))
        time.sleep(0.5)
        acceptCookiesBtn.click()
    except: pass

    username = "paige420x"
    password = "Paige1337"

    userInputElement = W(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    passInputElement = W(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    try:
        acceptCookiesBtn = W(driver, 10).until(EC.element_to_be_clickable((By.ID, "cookiePopupAcceptEU")))
        time.sleep(0.5)
        acceptCookiesBtn.click()
    except: pass
    time.sleep(1)
    ActionChains(driver).move_to_element(userInputElement).click().perform()
    type_keys(userInputElement, username)
    time.sleep(0.3)
    ActionChains(driver).move_to_element(passInputElement).click().perform()
    type_keys(passInputElement, password)
    time.sleep(0.2)

    loginBtn = driver.find_element(By.XPATH, '//*[@id="login_form"]/div[4]/button')
    ActionChains(driver).move_to_element(loginBtn).click().perform()

    print("Please confirm login in app within 60 seconds.")
    W(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
    print("Login Success")


    time.sleep(10)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    massMessage()
    
    time.sleep(60)


login()