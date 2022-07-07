"""
https://www.google.com/travel/flights/search?tfs=CBwQAhoyagwIAhIIL20vMDEzeXESCjIwMjItMDYtMjdyDAgCEggvbS8wcGx5MCgA QBFIFFAAWBcaMmo MCAISCC9tLz BwbHkwEgoyMDIyLTA2LTMwcgwIAhIIL20vMDEzeXEoAEARSBRQAFgXcAGCAQsI____________AUABSAGYAQE&gl=US&curr=USD
https://www.google.com/travel/flights/search?tfs=CBwQAhoqagwIAhIIL20vMDEzeXESCjIwMjItMDYtMjdyDAgCEggvbS8wcGx5MCgA GipqDAgCEggvbS8wcGx5MBIKMjAyMi0wNi0zMHI MCAISCC9tLz AxM3lxKABwAYIBCwj___________8BQAFIAZgBAQ&gl=US&curr=USD
f"https://www.google.com/travel/flights?q=Flights%20to%20{self.destination}%20from%20{self.origin}%20on%20{journey['outgoing']}%20through%20{journey['incoming']}%20economy%20class%20nonstop&curr=USD
https://www.google.com/travel/flights?q=Flights%20to%20MCO%20from%20ATL%20on%202022-06-27%20through%202022-06-30%20economy%20class%20nonstop&curr=USD&gl=US"
https://www.google.com/travel/flights?q=Flights%20to%20MCO%20from%20ATL%20on%202022-06-14%20through%202022-06-16%20economy%20class%20nonstop&curr=USD

"""
import re
from genericpath import isfile
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from BaseCall import BaseCall
from EmailSender import send_email


class AtlMco(BaseCall):
    
    def __init__(self):
        super().__init__()
        self.takeoff_1 = "1200,1600"
        self.takeoff_2 = "1700,2100"
        self.origin = "ATL"
        self.destination = "MCO"
        
    def make_url(self, journey):
        url = f"https://www.google.com/travel/flights?q=Flights%20to%20{self.destination}%20from%20{self.origin}%20on%20{journey['outgoing']}%20through%20{journey['incoming']}%20economy%20class%20nonstop&curr=USD&gl=US"
        return url

    def send_request(self, url):
        time_from, time_to = 17, 21
        self.browser.get(url)
        self.browser.implicitly_wait(30)    
        
        times_button_xpath = "button[aria-label='Times, Not selected']"
        self.browser.find_element(by=By.CSS_SELECTOR, value=times_button_xpath).click()
        time.sleep(3)
        
        action_chains = ActionChains(self.browser)
        # OUTBOUND
        ##yDmH0d > div.ynHwec.ZApNje.eXUIm > div.xkSIab > div > div.i4ijO > div > div.ztrQMe.gBIxsf > section.uq4A8e.Ud9qge.d18Cgb.S6pwD > div > div > div > div:nth-child(3) > span > div > div:nth-child(2) > div > div.TkG0O > div > div > div:nth-child(4)
        
        #"div[jsname='PFprWc'][jscontroller='OaKrge'][class='VfPpkd-UTM9ec VfPpkd-ksKsZd-mWPk3d VfPpkd-ksKsZd-mWPk3d-OWXEXe-ZNMTqd VfPpkd-ksKsZd-mWPk3d-OWXEXe-Tv8l5d-lJfZMc VfPpkd-UTM9ec-OWXEXe-XpnDCe VfPpkd-UTM9ec-OWXEXe-SfQLQb-uDEFge']"
        #//*[@id="yDmH0d"]/div[8]/div[3]/div/div[2]/div/div[1]/section[5]/div/div/div/div[2]/span/div/div[2]/div/div[2]/div/div/div[2]
        outbound_slider_from_selector = "div[class='dq93Ae Vt0wLe lqK3vd cmKkVe eXUIm'] > div[class='xkSIab'] > div[class='AJUxkf'] > div[class='moxAJc LZgQXe'] > section['uq4A8e Ud9qge'] > div[class='PPUsDb'] > div[jsname='d417mf'] > div[jsname='uxAMZ'] > div[aria-labelledby='id_0'] > span > div[class='CkYpqe'] > div[class='PlyoXe'] > div[class='J6LnA'] > div[class='TkG0O'] > div > div:nth-child(4)"
        outbound_slider_from_element = self.browser.find_element(by=By.CSS_SELECTOR, value=outbound_slider_from_selector)
        outbound_time_from_selector = "input[class='VfPpkd-YCNiv'][aria-label='Departure'][type='range'][min='0']"
        time_from_element = self.browser.find_element(by=By.CSS_SELECTOR, value=outbound_time_from_selector)
        time_from_value = time_from_element.get_attribute("value")
        while time_from_value != time_from:
            action_chains.click_and_hold(outbound_slider_from_element).move_by_offset(1, 0).release()
            action_chains.perform()
            time.sleep(1)
        time.sleep(3)
        outbound_slider_to_selector = "div[jsname='PFprWc'][jscontroller='OaKrge'][class='VfPpkd-UTM9ec VfPpkd-UTM9ec-OWXEXe-XpnDCe VfPpkd-UTM9ec-OWXEXe-SfQLQb-uDEFge VfPpkd-ksKsZd-mWPk3d-OWXEXe-Tv8l5d-lJfZMc VfPpkd-ksKsZd-mWPk3d VfPpkd-ksKsZd-mWPk3d-OWXEXe-ZNMTqd']"
        outbound_slider_to_element = self.browser.find_element(by=By.CSS_SELECTOR, value=outbound_slider_to_selector)
        outbound_time_to_selector = "input[class='VfPpkd-YCNiv'][aria-label='Departure'][type='range'][max='24']"
        outbound_time_to_element = self.browser.find_element(by=By.CSS_SELECTOR, value=outbound_time_to_selector)
        time_to_value = outbound_time_to_element.get_attribute("value")
        while time_to_value != time_to:
            action_chains.click_and_hold(outbound_slider_to_element).move_by_offset(-1, 0).release()
            action_chains.perform()
            time.sleep(3)
        time.sleep(3)

        # RETURN

    def parse_website(self):
        #//*[@id="yDmH0d"]/*/span
        #//*[@id="yDmH0d"]/span
        
        price_xpath = "//div[contains(@class, 'YMlIz FpEdx')]/span"
        prices = [el.text for el in self.browser.find_elements(by=By.XPATH, value=price_xpath)]    
        return prices

    def save_to_file(self, prices, journey, file):
        
            airports = f"{self.origin}-{self.destination}"
            fieldnames =["airports", "outgoing", "incoming", "price"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not isfile("/tmp/flight_prices.csv"):
                writer.writeheader()
            for price in prices[:10]:
                price = re.sub("[USD$]", "", price)
                print(price)
                writer.writerow({"airports": airports, "outgoing": journey['outgoing'], "incoming": journey['incoming'], "price": price})

    def execute(self):
        self.make_journeys(7, 5)
        self.make_journeys(30, 5)
        with open("/tmp/flight_prices.csv", "a", newline='') as file:
            for journey in self.journeys:
                url = self.make_url(journey)
                self.send_request(url)
                prices = self.parse_website()
                time.sleep(5)
                self.save_to_file(prices, journey, file)
                time.sleep(5)
        send_email(self.origin, self.destination)
        print(f"Sent email with {self.origin}-{self.destination} for dates {journey['outbound']}-{journey['returning']}")