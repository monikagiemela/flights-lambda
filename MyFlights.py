#cabin=p,e,bfbe;
# "https://www.{site}/{self.origin}-{self.destination}/{journey['outbound']}/{journey['returning']}?fs=takeoff={self.takeoff_1}__{self.takeoff_2};stops=0;airports={self.origin},{self.destination}&sort=price_a"
# https://www.esky.pl/flights/select/roundtrip/ap/waw/mp/rom?departureDate=2022-08-13&filter%5Bstops%5D=0&pa=2&page=1&pc=0&pi=0&py=0&returnDate=2022-08-16&sc=economy
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
        self.origin = "waw"
        self.destination = "rom"
        self.sites = ["kayak.com/flights", "momondo.com/flight-search"]
        
    def make_url(self, journey):
        url = f"https://www.esky.pl/flights/select/roundtrip/ap/{self.origin}/mp/{self.destination}?departureDate={journey['outbound']}&filter%5Bstops%5D=0&pa=2&page=1&pc=0&pi=0&py=0&returnDate={journey['returning']}&sc=economy"
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
        #for site in self.sites:
        with open("/tmp/flight_prices.csv", "w", newline='') as file:
            for journey in self.journeys:
                url = self.make_url(journey)
                prices = self.send_request(url)
                time.sleep(5)
                self.save_to_file(prices, journey, file)
                time.sleep(5)
        send_email(self.origin, self.destination, url)
        print(f"Sent email with {self.origin}-{self.destination} for dates {journey['outbound']}-{journey['returning']}")