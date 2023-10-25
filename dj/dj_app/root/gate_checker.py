from .root_class import Root_class


# this class subclassess Root_class that creates instance variables of the subclass and inherits its methods
class Gate_checker(Root_class):
    
    def __init__(self,):

        # super method inherits all of the instance variables of the Gate_root class.
        super().__init__()


    def ewr_UA_gate(self, query=None):
        # Stacking query items together
        # update actual more frequently and scheduled less frequently. maybe couple times a day for scheduled
        master = self.load_master()
        flights = []
        for flt_num, values in master.items():
            gate = values[0]
            scheduled = values[1]
            actual = values[2]
            
            if f'{query}' in gate:
                flights.append({
                    'gate': gate,
                    'flight_number': flt_num,
                    'scheduled': scheduled,
                    'actual': actual,
                })

        # Sorts the date by 'scheduled' in descending order to get the latest date and time to the top
        flights = sorted(flights, key=lambda x:x['scheduled'], reverse=True)

        # Converting it back to string for it to show in a viewable format otherwise
            # browser craps out when it sees class object for date since earlier 'scheduled' item is a class object and not a string
        for dictionries in flights:
            dictionries['scheduled'] = dictionries['scheduled'].strftime("%#H:%M, %b%d")
            dictionries['actual'] = dictionries['actual'].strftime("%#H:%M, %b%d")
        
        return flights
    
    