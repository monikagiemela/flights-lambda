from os import path
import time
import csv
from BaseCall import BaseCall
from EmailSender import send_email


class LgaOrd(BaseCall):
    
    def __init__(self):
        super().__init__()
        self.takeoff_1 = "1100,1500"
        self.takeoff_2 = "1100,1500"
        self.origin = "LGA"
        self.destination = "ORD"
     
    def make_url(self, journey):
        url = f"https://www.kayak.com/flights/{self.origin}-{self.destination}/{journey['outbound']}/{journey['returning']}?fs=takeoff={self.takeoff_1}__{self.takeoff_2};cabin=-b,f;stops=0;airports={self.origin},{self.destination}&sort=price_a" 
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
        self.make_journeys(7, 4)
        self.make_journeys(30, 4)
        with open("/tmp/flight_prices.csv", "w", newline='') as file:
            for journey in self.journeys:
                url = self.make_url(journey)
                prices = self.send_request(url)
                time.sleep(5)
                self.save_to_file(prices, journey, file)
                time.sleep(5)
        send_email(self.origin, self.destination)
        print(f"Sent email with {self.origin}-{self.destination} for dates {journey['outbound']}-{journey['returning']}")