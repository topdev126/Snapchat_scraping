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
ua = UserAgent()

def type_keys(element: WebElement, text: str):
    for character in text:
        delay = random.uniform(0.1, 0.2)
        element.send_keys(character)
        time.sleep(delay)

chrome_options = ChromeOptions()
#chrome_options.add_argument('--user-agent="' + ua.chrome + '"')
print(ua.chrome)
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-site-isolation-trials")
chrome_options.add_argument("--disable-application-cache")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument("--incognito")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#chrome_options.add_experimental_option("prefs", {"useAutomationExtension": "False", "excludeSwitches": "enable-automation"})
chrome_options.add_argument('--ignore-certificate-errors')

chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"')

#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')

dPath = os.path.join(os.path.dirname(__file__),"./chromedriver")
driver = Chrome(executable_path=dPath, options=chrome_options)

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source":
        "const newProto = navigator.__proto__;"
        "delete newProto.webdriver;"
        "navigator.__proto__ = newProto;"
})

def loadAllMessages():
    messagesBox = driver.find_element(By.XPATH, "//div[@aria-label='grid']")
    time.sleep(1)

    verical_ordinate = 100
    for i in range(0, 300):
        print(str(verical_ordinate))
        driver.execute_script("arguments[0].scrollTop = arguments[1]", messagesBox, verical_ordinate)
        verical_ordinate += 100
        time.sleep(0.1)

def massMessage():
    #driver.get("http://web.snapchat.com")
    time.sleep(5)
    print("Loading all messages, this can take some time..")
    loadAllMessages()
    print("All messages have been loaded.")
    messagesBox = driver.find_element(By.XPATH, "//div[@aria-label='grid']")
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", messagesBox)

    messages = driver.find_elements(By.XPATH, "//div[@class='O4POs']")

    #for i in range(len(messages)):
    #    print("message found")
    #    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", messagesBox)

    #print("Counted: ", len(messages), "chats.")
    msgCount = driver.find_elements(By.XPATH, "//div[@role='gridcell']")
    print(len(msgCount), " Chats found.")

def sendMessage(message):
    driver.get("http://web.snapchat.com")
    driver.find_elements(By.XPATH, "//span[normalize-space()='New Chat']")[0].click()
    messageField = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@placeholder='Send a Chat']")))
    ActionChains(driver).move_to_element(messageField).click().perform()
    type_keys(messageField, message)
    messageField.send_keys(Keys.ENTER)
    chatName = driver.find_element(By.XPATH, "/html[1]/body[1]/main[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]/span[1]/span[1]").text
    print("Debug: Message sent to: ", chatName)

    closeChat = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@title='Close Chat']//*[name()='svg']")))
    ActionChains(driver).move_to_element(closeChat).click().perform()

def uploadStory():
    driver.get("http://my.snapchat.com")

    if W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Sign in']"))):
        doubleLogin = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Sign in']")))
        ActionChains(driver).move_to_element(doubleLogin).click().perform()

    storyPostToggle = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-1cuc575']//div[2]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//div[2]//div[1]//button[1]//*[name()='svg']")))
    ActionChains(driver).move_to_element(storyPostToggle).click().perform()
    time.sleep(1)

    imagePath = os.path.join(os.path.dirname(__file__),"image.jpg")

    uploadInput = driver.find_element(By.XPATH, "//input[@type='file']")
    uploadInput.send_keys(imagePath)
    try:
        W(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-gbtqlk']//div//*[name()='svg']//*[name()='path' and contains(@fill-rule,'evenodd')]")))
        #image upload success
        pass
    except:
        #image upload fail, handle it..
        print("Image upload failed")
    postToStory = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Post to Snapchat']")))
    ActionChains(driver).move_to_element(postToStory).click().perform()
    storyPostSuccess = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-0']//div[@class='css-ns68x5'][normalize-space()='Posted to My Story']")))
    if storyPostSuccess:
        print("Story post successfull")
        closeBtn = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Close']")))
        ActionChains(driver).move_to_element(closeBtn).click().perform()
    time.sleep(30)

def scheduleStoryPost():
    driver.get("http://my.snapchat.com")
    if W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Sign in']"))):
        doubleLogin = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Sign in']")))
        ActionChains(driver).move_to_element(doubleLogin).click().perform()

    storyPostToggle = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-1cuc575']//div[2]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//div[2]//div[1]//button[1]//*[name()='svg']")))
    ActionChains(driver).move_to_element(storyPostToggle).click().perform()
    time.sleep(0.5)
    storyScheduleToggle = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-1cuc575']//div//div//div//div//div[@class='css-1ltqc89 sds-card sds-container css-138x76l']//button[@type='button']//*[name()='svg']")))
    ActionChains(driver).move_to_element(storyScheduleToggle).click().perform()
    time.sleep(1)

    curTime = driver.find_element(By.XPATH, "//input[@placeholder='Select date']").get_attribute("value")
    curTimezone = driver.find_element(By.XPATH, "//div[@role='combobox']").text
    postTime = driver.find_element(By.XPATH, "//input[@placeholder='Select date']")
    print("Current time: ", curTime)
    print("Detected timezone: ", curTimezone)
    scheduledTime = "2022-12-12 15:00"
    driver.execute_script("arguments[0].removeAttribute('readonly')", postTime)
    postTime.clear()
    driver.execute_script("arguments[0].value = '" + str(scheduledTime) + "';", postTime) 
    time.sleep(30)
  
    imagePath = os.path.join(os.path.dirname(__file__),"image.jpg")

    uploadInput = driver.find_element(By.XPATH, "//input[@type='file']")
    uploadInput.send_keys(imagePath)

    try:
        W(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-gbtqlk']//div//*[name()='svg']//*[name()='path' and contains(@fill-rule,'evenodd')]")))
        #image upload success
        pass
    except:
        #image upload fail, handle it..
        print("Image upload failed")
    schedulePost = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Schedule Snap']")))
    ActionChains(driver).move_to_element(schedulePost).click().perform()


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

    username = "paigetodayx"
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

    #confirmNotice = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='tiv-h2 tiv-verifyCardTitle']")))
    #if confirmNotice:
    #    confirmInApp = driver.find_element(By.XPATH, "//div[@class='tiv-h2 tiv-verifyCardTitle']").text
    #    if confirmInApp == "Confirm in Snapchat":
    #        needLoginConfirm = True
    #        print("Please confirm login in Snapchat app within 60 seconds")

    time.sleep(10)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    print("Debug: Counting messages")

    potentialWelcomeMsgs = len(driver.find_elements(By.XPATH, "//span[normalize-space()='Say hi!']"))
    print("Potential Welcome Messages: ", potentialWelcomeMsgs)

    newSnaps = len(driver.find_elements(By.XPATH, "//span[normalize-space()='New Snap']"))
    print("New snaps: ", newSnaps)

    newChats = len(driver.find_elements(By.XPATH, "//span[normalize-space()='New Chat']"))
    print("New chats: ", newChats)

    leftOnRead = len(driver.find_elements(By.XPATH, "//span[normalize-space()='Received']"))
    print("You have left ", leftOnRead, "people on read..")

    #sendMessage("Hi again...")
    #uploadStory()
    #scheduleStoryPost()
    massMessage()
    time.sleep(60)
    #driver.quit()


login()