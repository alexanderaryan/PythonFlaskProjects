from selenium import webdriver
import getpass
import time
from selenium.webdriver.common.by import By


class Automate:
    def __init__(self, passwrd , userinput):
        self.passwrd = passwrd

        chrome_options = webdriver.ChromeOptions()

        self.prefs = {"profile.default_content_setting_values.notifications" : 2}

        chrome_options.add_experimental_option("prefs",self.prefs)

        self.driver = webdriver.Chrome("D:\Localgit\chromedriver.exe",chrome_options=chrome_options)
        if userinput.lower() == 'f':
            self.driver.get('https://www.facebook.com/')
        elif userinput == 't':
            self.driver.get('https://twitter.com/login')

    def posting(self, post):

        username = f.driver.find_element_by_id('email')
        username.send_keys('wmamjmtmdg')
        password = f.driver.find_element_by_id('pass')
        password.send_keys(self.passwrd)

        login = self.driver.find_element_by_id('loginbutton')
        login.click()

        postspace = self.driver.find_element_by_name('xhpc_message')
        postspace.click()
        postspace.send_keys(post)

        buttons = self.driver.find_elements_by_tag_name('button')
        for button in buttons:
            if button.text == 'Post':
                button.click()


    def tweeting(self, tweet):
            username = self.driver.find_element_by_class_name('js-username-field')
            username.send_keys('alex.playboy.ander@gmail.com')

            password = self.driver.find_element_by_class_name('js-password-field')
            print(passwrd)
            password.send_keys(passwrd)
            # time.sleep(2)
            login = self.driver.find_element_by_css_selector('button.submit.EdgeButton.EdgeButton--primary.EdgeButtom--medium')
            login.submit()

            time.sleep(5)
            postspace = self.driver.find_element_by_class_name('public-DraftStyleDefault-block')
            postspace.click()
            postspace.send_keys(tweet[0:139])
            print (len(tweet))

            if len(tweet)<140:

                button = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div[3]')
                #button = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div[2]/a')
                button.click()
            else:
                button = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div[2]/a')
                button.click()
                listtweet = []
                for l in range(140,len(tweet),139):
                    listtweet.append(tweet[l:l+139])
                print (listtweet)
                print (len(listtweet), " is the length")
                for n in range(1,len(listtweet)+1):
                    print (n)
                    postspace = self.driver.find_elements_by_class_name('public-DraftStyleDefault-block')
                    print(postspace)
                    postspace[n].send_keys(listtweet[n-1])
                    if n<len(listtweet):
                        xpath='//*[@id="react-root"]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div['+str(n+1)+']/div/div/div/div[2]/div[2]/div/div/div[2]/div[3]'
                        print (xpath)
                        addbutton = self.driver.find_element_by_xpath(xpath)
                        self.driver.execute_script("arguments[0].scrollIntoView();", addbutton)
                        addbutton.click()



                # postspace[-1].click()

                # postspace[0].send_keys("Just adding few more tweets messages to make it a thread. I don't know what else to type to make total words higher that 140. So typing whatever comes to mind. Please bear with me for sometimes. Then I will come up with an idea to chunk 140 characters per tweet!! #GoPython")

                #postspace[1].send_keys(tweet[139:])

                # tweet = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div[4]/div')
                # tweet = driver.find_element_by_class_name('css-901oao')
                #time.sleep(5)
                tweet = self.driver.find_element_by_css_selector('div.css-18t94o4.css-1dbjc4n.r-urgr8i.r-42olwf.r-sdzlij.r-1phboty.r-rs99b7.r-1w2pmg.r-1n0xq6e.r-1vuscfd.r-1dhvaqw.r-1fneopy.r-o7ynqc.r-6416eg.r-lrvibr')
                # react-root > div > div > div.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-184en5c > div > div > div > div > div.css-1dbjc4n.r-1habvwh.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv > div.css-1dbjc4n.r-t23y2h.r-1wbh5a2.r-rsyp9y.r-1pjcn9w.r-htvplk.r-1udh08x.r-1potc6q > div > div.css-1dbjc4n.r-16y2uox.r-1wbh5a2.r-1jgb5lz.r-1ye8kvj.r-13qz1uu > div > div > div:nth-child(2) > div > div > div > div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-15d164r.r-5f2r5o.r-1bylmt5.r-13tjlyg.r-7qyjyx.r-1ftll1t > div:nth-child(2) > div > div > div:nth-child(2) >
                #time.sleep(15)
                tweet.send_keys('\n')




if __name__ == '__main__':
    while True:
        try:
            user_input = input("You wanna Post or Tweet? Type F or T or E(exit)... : ")[0].lower()
        except:
            print ("Type only F or T")
            continue
        else:
            if user_input.lower() not in ('f','t'):
                print("Type only F or T")
                continue
            else:
                if user_input == 'f':
                    passwrd = getpass.getpass(prompt="Enter your facebook password : ")
                    post = input("Enter your Post : ")
                    f = Automate(passwrd, user_input)
                    f.posting(post)
                    break
                elif user_input == 't':
                    passwrd = getpass.getpass(prompt="Enter your Twitter password : ")
                    tweet = input("Type your tweet here : ")
                    t = Automate(passwrd,user_input)
                    t.tweeting(tweet)
                    break
                else:
                    print ("Thank you for using me. Bye Bye!!!!!")

