from selenium import webdriver
import getpass
import time
from selenium.webdriver.common.by import By
passwrd = getpass.getpass(prompt="Enter your facebook password : ")
chrome_options = webdriver.ChromeOptions()

prefs = {"profile.default_content_setting_values.notifications" : 2}

chrome_options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome("D:\Localgit\chromedriver.exe",chrome_options=chrome_options)
#driver = webdriver.Chrome("D:\Localgit\chromedriver.exe")

driver.get('https://www.facebook.com/')

def facebooklogin(passwrd):


    username = driver.find_element_by_id('email')
    username.send_keys('wmamjmtmdg')

    password = driver.find_element_by_id('pass')

    password.send_keys(passwrd)

    login = driver.find_element_by_id('loginbutton')
    login.click()


    postspace = driver.find_element_by_name('xhpc_message')
    postspace.click()
    postspace.send_keys('Hello Friends!! Trying to Automate my Facebook posts using Python and Selenium WebDriver!!')


    buttons = driver.find_elements_by_tag_name('button')
    for button in buttons:
        if button.text == 'Post':
            button.click()



if __name__ == '__main__':



    facebooklogin(passwrd)