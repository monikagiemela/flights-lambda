import json
from datetime import datetime
from Flight_Scrapers.LaxJfk import LaxJfk
from Flight_Scrapers.LgaOrd import LgaOrd
from Flight_Scrapers.DfwOrd import DfwOrd
#from AtlMco import AtlMco

def lambda_handler(event, context):
    print("Initializing CRON Schedular.... ")

    if datetime.today().isoweekday() == 1:
        lax_jfk = LaxJfk()
        lax_jfk.execute()

    elif datetime.today().isoweekday() == 2:
        lga_ord = LgaOrd()
        lga_ord.execute()

    elif datetime.today().isoweekday() == 3:
        dfw_ord = DfwOrd()
        dfw_ord.execute()
    
    #atl_mco = AtlMco()
    #atl_mco.execute()
