from django.shortcuts import render
from .models import SearchQuery
from .root.gate_checker import Gate_checker
from .root.gate_scrape import Gate_scrape_thread
from .root.MET_TAF_parse import Weather_display
from .root.dep_des import Pull_flight_info
# from .root.flt_deet import airports


'''
views.py runs as soon as the base web is requested. Hence, GateCheckerThread() is run the background right away.
It will then run 
'''
run_lengthy_web_scrape = False 

if run_lengthy_web_scrape:
    'Running Lengthy web scrape'
    gc_thread = Gate_scrape_thread()
    gc_thread.start()

current_time = Gate_checker().date_time()


def home(request):
    # Homepage first skips a "POST", goes to else and returns home.html since the query is not submitted yet.
    if request.method == "POST":
        main_query = request.POST.get('query','')
        
        # This one adds similar queries to the admin panel in SearchQuerys.
        # Make it such that the duplicates are grouped using maybe unique.
        search_query = SearchQuery(query=main_query)      # Adds search queries to the database
        search_query.save()                               # you've got to save it otherwise it wont save
        
        return parse_query(request, main_query)

    else:
        return render(request, 'home.html')


def parse_query(request, main_query):
    main_query = main_query
    query_in_list_form = []     # Global variable since it is used outside of the if statement in case it was not triggered. purpose: Handeling Error
                                    # if .split() method is used outside here it can return since empty strings cannot be split.
                                    
    if main_query == '':        # query is empty then return all gates
        return gate_info(request, main_query='')
    if main_query != '':        # if query is not empty it splits it into list form
        query_in_list_form = main_query.split()
        if len(query_in_list_form) == 1:            # If query is only one word or item  
            query = query_in_list_form[0].upper()           # this is string form instead of list
            if 'A' in query or 'B' in query or 'C' in query or len(query)==1:
                # When the length of query_in_list_form is only 1 it returns gates table for that particular query.
                gate_query = query
                return gate_info(request, main_query=gate_query)
            elif query[:2] == "UA":
                return flight_deets(request, query[2:])
            elif len(query) == 4 or len(query) == 3 or len(query) == 2:
                if query.isdigit():
                    # if betwee 1 to 35 for A, between 40-70 for B between 70-135 for c
                    query = int(query)
                    if 1 <= query <= 35 or 40 <= query <= 136:
                        return gate_info(request, main_query=str(query))
                    else:    
                        return flight_deets(request, query)
                else:
                    return gate_info(request, main_query=str(query))

    if len(query_in_list_form) > 1:
        first_letter = query_in_list_form[0].upper()        # Making it uppercase for compatibility issues and error handling
        if first_letter == 'W':
            weather_query_airport  = query_in_list_form[1]
            weather_query_airport = weather_query_airport.upper()       # Making query uppercase for it to be compatible
            return metar_display(request, weather_query_airport)

        if first_letter == 'I':        
            return flight_deets(request, query_in_list_form)
        else:       # If the query is not recognized:
            return gate_info(request, main_query=main_query)
            '''
            # Attempting to pull all airports for easier search access
            florida_airports = airports['Florida'][1]
            for each_airport in florida_airports:
                if each_query in each_airport:
                    print(each_airport)
                flights = Gate_checker().departures_ewr_UA()
                print(3)
                for flt in flights:
                    # print(flt)
                    if each_query in flt:
                        print(4)
                        return flight_deets(request, abs_query, flt)
                    else:
                        # return a static html saying no information found for flight number ****
                        pass'''


def gate_info(request,main_query):
    gate = main_query
    # In the database all the gates are uppercase so making the query uppercase    
    gate = gate.upper()

    # Dictionary format a list with one or many dictionaries each dictionary containing 4 items:gate,flight,scheduled,actual

    current_time = Gate_checker().date_time()
    gate_data_table = Gate_checker().ewr_UA_gate(gate)

    # showing info if the info is found else it falls back to `No flights found for {{gate}}`on flight_info.html
    if gate_data_table: 
        # print(gate_data_table)
        return render(request, 'flight_info.html',{'gate_data_table': gate_data_table, 'gate': gate, 'current_time': current_time})
    else:       # Returns all gates since query is empty. Maybe this is not necessary. Try deleting else statement.
        return render(request, 'flight_info.html', {'gate': gate})


def flight_deets(request, query_in_list_form ):
    # given a flight number it returns its, gates, scheduled and actual times of departure and arrival

    flt_info = Pull_flight_info()           # from dep_des.py file
    bulk_flight_deets = flt_info.pull_UA(query_in_list_form)

    def weather_req(airport):
        weather = Weather_display()         # from MET_TAF_parse.py
        weather = weather.scrape(airport)
        return weather

    dep_weather = weather_req(bulk_flight_deets['departure_ID'])
    dest_weather = weather_req(bulk_flight_deets['destination_ID'])
    weather = {'dep_weather':dep_weather, 'dest_weather': dest_weather}

    bulk_flight_deets.update(weather)

    return render(request, 'flight_deet.html', bulk_flight_deets)


def metar_display(request,weather_query):
    
    weather_query = weather_query.strip()       # remove leading and trailing spaces. Seems precautionary.
    airport = weather_query[-4:]
    
    weather = Weather_display()
    weather = weather.scrape(weather_query)
    
    return render(request, 'metar_info.html', {'airport': airport, 'weather': weather})


def contact(request):
    return render(request, 'contact.html')


def ourstory(request):
    return render(request, 'ourstory.html')


def source(request):
    return render(request, 'source.html')


def gate_check(request):
    return render(request, 'gate_check.html')


def flight_lookup(request):
    return render(request, 'home.html', {'flight_lookup': True})


def weather(request):
    return render(request, 'weather.html')
    

def guide(request):
    return render(request, 'guide.html')

def report_an_issue(request):
    return render(request, 'report_an_issue.html')

