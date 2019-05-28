from selenium import webdriver
from multiprocessing import Process
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup as soup
from flask import Flask

cookies = ''
app = Flask(__name__)

@app.route('/')
def homepage():
    options = webdriver.ChromeOptions()
    # options.add_argument('disable-infobars')        
    options.add_argument('--no-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--headless')
    options.add_argument('--dump-dom')

    url = 'https://logon7.gov.bc.ca/clp-cgi/capBceid/logon.cgi?flags=0100:0,8&TYPE=33554433&REALMOID=06-60cd9873-d985-43fe-8070-5a6a1d1fc284&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=$SM$HU19nngfcumBlpv%2f1Vh%2fVYA9CwcRmY0%2bNDHmmacZYjHSIMZku%2fy%2fCtmfFQPxTOIz637zJFQB0hiY5PezwoGff055NxdAEcw1&TARGET=$SM$https%3a%2f%2fskillstraininggrants%2egov%2ebc%2eca%2fExt%2fHome'
    driver = webdriver.Chrome(executable_path='chromedriver', options=options)
    # driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    driver.get(url)

    #USER MUST CHOOSE TO LOGIN
    global cookies
    cookies = driver.get_cookies()
    elem = WebDriverWait(driver, 3600).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[1]/a"))
    )


    #EXECUTE JAVASCRIPT TO ADD NAVBARS
    def skin(driver):
        driver.execute_script("""
                        document.body.innerHTML = "<div class='main-main-container'>" + document.body.innerHTML + "</div>"
                        document.head.innerHTML = `<link href='http://fonts.googleapis.com/css?family=Roboto+Condensed' rel='stylesheet' type='text/css'>
                    <style>
                    * {
                      margin: 0;
                      padding: 0;
                    }
    
                    html {
                      font-size: 24px;
                      font-family: 'Roboto Condensed';
                    }
    
                    body {
                      background-color: #fafafa;
                    }
    
                    nav {
                      position: fixed;
                      height: 100%;
                      width: 65%;
                    }
                    nav::before {
                      content: '';
                      display: inline-block;
                      width: 0;
                      height: 100%;
                      vertical-align: middle;
                    }
                    nav > ul {
                      width: 80%;
                      display: inline-block;
                      vertical-align: middle;
                    }
                    nav > ul > li {
                      display: block;
                      text-transform: uppercase;
                      line-height: 2;
                      font-size: .8rem;
                      padding-left: 30%;
                    }
    
                    .hamburger {
                      left: 1rem;
                      top: 1rem;
                      width: 1.5rem;
                      height: .7rem;
                      position: fixed;
                      z-index: 2;
                      cursor: pointer;
                    }
                    .hamburger > span {
                      display: block;
                      background-color: #262626;
                      height: 20%;
                      margin-bottom: 20%;
                    }
    
                    .main-main-container {
                      position: fixed;
                      top: 0;
                      left: 0;
                      right: 0;
                      bottom: 0;
                      background-color: #fafafa;
                      color: #262626;
                      padding: 4rem;
                      overflow: auto;
                      transition: .2s ease;
                    }
                    @media screen and (orientation: portrait) {
                      .main-main-container {
                        padding: 4rem 1rem;
                      }
                    }
                    .main-main-container a {
                      color: #00c7be;
                    }
                    .main-main-container > p {
                      padding-bottom: 1em;
                    }
                    .main-main-container > h4 {
                      margin: 1em 0;
                    }
    
                    @media screen and (orientation: portrait) {
                      nav.active + .main-main-container {
                        transform: translateX(55%) scale(0.8);
                        box-shadow: 0 0 30px 5px rgba(38, 38, 38, 0.3);
                      }
                    }
                    @media screen and (orientation: landscape) {
                      nav.active + .main-main-container {
                        transform: translateX(35%) scale(0.8);
                        box-shadow: 0 0 30px 5px rgba(38, 38, 38, 0.3);
                      }
                    }
                    </style>` + document.head.innerHTML;
    
                        document.body.innerHTML = `<nav>
                      <ul>
                        <li><a href="">Create App</a></li>                  
                        <li><a href="">Create Placeholders</a></li>
                        <li><a href="">View Training Planner</a></li>
                      </ul>
                    </nav>` + document.body.innerHTML + `<div class="hamburger">
                <span></span>
                <span></span>
                    <span></span>
                    </div>`;
                    $(".hamburger").click(function() {
                    $("nav").toggleClass("active");
                    });""")

    skin(driver)

    #CONTINUE TO SHOW THE NAVBAR SKIN AS LONG AS USER IS LOGGED IN
    while True:
        try:
            page = soup(driver.page_source,'html.parser')
            find = page.find('div',{'class':'main-main-container'})
            if len(find) > 1:
                pass
        except Exception:
            if 'skillstraininggrants' not in driver.current_url:
                pass
            else:
                time.sleep(0.5)
                skin(driver)
                pass


#THIS IS THE AUTOMATED DATA ENTRY
@app.route('/build')
def build():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome('chromedriver')
    # driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://google.com')
    driver.add_cookie(cookies)
    driver.get('https://skillstraininggrants.gov.bc.ca/Ext/Home?')

    #AUTMOATED DATA ENTRY GOES HERE.

if __name__ == '__main__':
    app.run()
