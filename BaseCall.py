import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from tempfile import mkdtemp
from params import make_day_params


class BaseCall:    
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--start-fullscreen')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-dev-tools")
        chrome_options.add_argument("--no-zygote")
        chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
        chrome_options.add_argument(f"--data-path={mkdtemp()}")
        chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        chrome_options.add_argument("--remote-debugging-port=9222")
        self.browser = webdriver.Chrome("/opt/chromedriver",options=chrome_options)
        self.journeys = []
    
    def make_journeys(self, outgoing_delta, return_delta):
        outbound, returning = make_day_params(outgoing_delta, return_delta)
        self.journeys.append({"outbound": outbound, "returning": returning})

    def send_request(self, url):
        self.browser.get(url)
        self.browser.implicitly_wait(30)
        time.sleep(45)
        # Close cookies pop-up
        try:
            self.browser.find_element(by=By.CLASS_NAME, value="bBPb-close").click()
        except (NoSuchElementException, ElementNotInteractableException):
            pass
        prices = [el.text for el in self.browser.find_elements(by=By.CLASS_NAME, value="price-text")]
        return prices