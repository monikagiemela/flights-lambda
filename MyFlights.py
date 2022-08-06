#cabin=p,e,bfbe;
from os import path
import time
import csv
from BaseCall import BaseCall
from EmailSender import send_email


class MyFlights(BaseCall):
    
    def __init__(self):
        super().__init__()
        self.takeoff_1 = "0700,1000"
        self.takeoff_2 = "1700,2100"
        self.origin = "WAW"
        self.destination = "ROM"
        self.sites = ["kayak.com/flights", "momondo.com/flight-search"]
        
    def make_url(self, journey, site):
        url = f"https://www.{site}/{self.origin}-{self.destination}/{journey['outbound']}/{journey['returning']}?fs=takeoff={self.takeoff_1}__{self.takeoff_2};stops=0;airports={self.origin},{self.destination}&sort=price_a" 
        return url

    def save_to_file(self, prices, journey, file):    
        airports = f"{self.origin}-{self.destination}"
        fieldnames =["airports", "outbound", "returning", "price"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not path.isfile("/tmp/flight_prices.csv"):
            writer.writeheader()
        for price in prices[:10]:
            price = price.replace("$", "")
            print(price)
            writer.writerow({"airports": airports, "outbound": journey['outbound'], "returning": journey['returning'], "price": price})

    def execute(self):
        self.make_journeys(14, 5)
        self.make_journeys(30, 5)
        for site in self.sites:
            with open("/tmp/flight_prices.csv", "w", newline='') as file:
                for journey in self.journeys:
                    url = self.make_url(journey, site)
                    prices = self.send_request(url)
                    time.sleep(5)
                    self.save_to_file(prices, journey, file)
                    time.sleep(5)
            send_email(self.origin, self.destination, url)
            print(f"Sent email with {self.origin}-{self.destination} for dates {journey['outbound']}-{journey['returning']}")