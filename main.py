from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pywhatkit
from datetime import datetime
from apscheduler.schedulers.background import BlockingScheduler

def ultimoPreso(browser):
    dateTime = browser.find_element(By.CSS_SELECTOR, ".normal > tbody > tr:nth-child(1) > td:nth-child(1)").text
    number = browser.find_element(By.CSS_SELECTOR, ".normal > tbody > tr:nth-child(1) > td:nth-child(2)").text
    description = browser.find_element(By.CSS_SELECTOR, ".normal > tbody > tr:nth-child(1) > td:nth-child(3)").text
    price = browser.find_element(By.CSS_SELECTOR, ".normal > tbody > tr:nth-child(1) > td:nth-child(4)").text

    messageLast = '\n---Ultimo Articolo---\nData e Ora: ' + dateTime + '\nNumero: ' + number + '\nNome: ' + description + '\nPrezzo: ' + price
    return messageLast

def checkGuadagno():
    usernameStr = '#####'
    passwordStr = '#####'
    PATH = "/PycharmProjects/botZellr/chromedriver"
    browser = webdriver.Chrome(PATH)
    browser.get('https://zellr.com/sovellus/guest.php?page=login')

    username = browser.find_element(By.ID, 'username')
    username.send_keys(usernameStr)
    password = browser.find_element(By.ID, 'password')
    password.send_keys(passwordStr)
    nextButton = browser.find_element(By.CLASS_NAME, 'button')
    nextButton.click()

    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar-menu"]/ul[1]/li[4]/a')))
    browser.find_element(By.XPATH, '//*[@id="sidebar-menu"]/ul[1]/li[4]/a').click()
    guadagno = browser.find_element(By.XPATH, "//*[@id='maincont']/table[1]/tbody/tr[1]/td[2]").text

    messageUltimo = ultimoPreso(browser)

    f = open("guadagno.txt", "r")
    old = f.read()

    old = float(old.replace(' CHF', ''))
    guadagnoComp = float(guadagno.replace(' CHF', ''))

    if guadagnoComp > old:
        with open('guadagno.txt', 'w') as f:
            f.write(guadagno)
            message = 'ZellrBot dice:\nNuovo saldo: ' + guadagno + messageUltimo
            pywhatkit.sendwhatmsg_instantly('+4179#######', message, 15, True)


    print(datetime.now())


def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(checkGuadagno, 'cron', day_of_week='mon-fri', hour="10-23", minute='5,15,25,35,45,55', timezone='UTC')
    scheduler.start()

if __name__ == "__main__":
    main()
