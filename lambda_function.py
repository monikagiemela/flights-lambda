#from datetime import datetime
#from LaxJfk import LaxJfk
#from LgaOrd import LgaOrd
#from DfwOrd import DfwOrd
#from AtlMco import AtlMco
from MyFlights import MyFlights

def lambda_handler(event, context):
    print("Initializing CRON Scheduler.... ")
    
    my_flights = MyFlights()
    my_flights.execute() 


#    if datetime.today().isoweekday() == 1:
#        lax_jfk = LaxJfk()
#        lax_jfk.execute()

#    elif datetime.today().isoweekday() == 2:
#        lga_ord = LgaOrd()
#        lga_ord.execute()

#    elif datetime.today().isoweekday() == 7:
#        dfw_ord = DfwOrd()
#        dfw_ord.execute()
    
    #atl_mco = AtlMco()
    
    #atl_mco.execute()
