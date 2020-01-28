from selenium import webdriver





driver = webdriver.Chrome("D:\Localgit\chromedriver.exe")
driver.get('https://web.whatsapp.com/')

input('Enter anything after scanning the QR code')
while True:
    name = input('Enter the name of user or group')
    msg = input('Enter your message')
    count = int(input('Enter the count'))
    user = driver.find_element_by_xpath('//span[@title ="{}"]'.format(name))
    user.click()

    msg_box = driver.find_element_by_class_name('_13mgZ')
    #_3FeAD _1PRhq

    for i in range(count):
        msg_box.send_keys(msg)
        button = driver.find_element_by_class_name('_3M-N-')
        button.click()

    retry = input("Wanna retry?Type Y or N")
    if retry.lower() =='n':
        break
    else:
        continue