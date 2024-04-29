import requests
import urllib.parse

KEY = "473cdd1a-6274-4cf4-8485-2ca79a23d1c9"

def geocoding(location, key):
    if key is None:
        key = KEY
    while location == "":
        location = input("Enter the location again: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1",
    "key":key})
    replydata = requests.get(url)
    json_data = replydata.json()
    open("geocode.json", "w").write(replydata.text)
    json_status = replydata.status_code
    if json_status == 200 and len(json_data["hits"]) !=0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country=""
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state=""
        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) !=0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        if len(value) != 0:
            new_loc = new_loc + " (" + value + ")"
        #print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)
    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status != 200:
            print("Geocode API status: " + str(json_status) + "\nError message: " + json_data["message"])
    return json_status,lat,lng, new_loc

##def ask_vehicle(): Not need anymore
##    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
##    print("Vehicle profiles available on Graphhopper:")
##    print("+++++++++++++++++++++++++++++++++++++++++++++")
##    print("car, bike, foot")
##    print("+++++++++++++++++++++++++++++++++++++++++++++")
##    profile=["car", "bike", "foot"]
##    vehicle = input("Enter a vehicle profile from the list above: ")
##    if vehicle == "quit" or vehicle == "q":
##        return None
##    elif vehicle in profile:
##        vehicle = vehicle
##    else:
##        vehicle = "car"
##        print("No valid vehicle profile was entered. Using the car profile.")
##    return vehicle

def routing_function(orig, dest, vehicle):
    route_url = "https://graphhopper.com/api/1/route?"
    op="&point="+str(orig[1])+"%2C"+str(orig[2])
    dp="&point="+str(dest[1])+"%2C"+str(dest[2])
    paths_url = route_url + urllib.parse.urlencode({"key":KEY, "vehicle":vehicle}) + op + dp
    paths_status = requests.get(paths_url).status_code
    paths_data = requests.get(paths_url).json()
    print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
    ##print("=================================================")
    ##print("Directions from " + orig[3] + " to " + dest[3] + " by " + vehicle)
    ##print("=================================================")
    ##if paths_status == 200:
    ##    print("Distance Traveled: " + str(paths_data["paths"][0]["distance"]) + "m")
    ##    print("Distance Traveled: {0:.1f} miles / {1:.1f} km".format(miles, km))
    ##    print("Trip Duration: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
    ##    print("=================================================")
    ##    for each in range(len(paths_data["paths"][0]["instructions"])):
    ##        path = paths_data["paths"][0]["instructions"][each]["text"]
    ##        distance = paths_data["paths"][0]["instructions"][each]["distance"]
    ##        print("{0} ( {1:.1f} km / {2:.1f} miles )".format(path, distance/1000, distance/1000/1.61))
    ##        print("=============================================")
    ##else:
    ##    print("Error message: " + paths_data["message"])
    ##    print("*************************************************")
    if paths_status != 200:
        print("Error message: " + paths_data["message"])
        print("*************************************************")
        return None
    data = {
        'origin': orig,
        'destination': dest,
        'm' : paths_data["paths"][0]["distance"],
        'miles' : (paths_data["paths"][0]["distance"])/1000/1.61,
        'km' : (paths_data["paths"][0]["distance"])/1000,
        'sec' : int(paths_data["paths"][0]["time"]/1000%60),
        'min' : int(paths_data["paths"][0]["time"]/1000/60%60),
        'hr' : int(paths_data["paths"][0]["time"]/1000/60/60),
        'instructions' : paths_data["paths"][0]["instructions"]
    }
    #get openStreetMap url using the instructions as one road
    url = f"https://www.openstreetmap.org/directions?engine={vehicle}&route={orig[1]}%2C{orig[2]}%3B{dest[1]}%2C{dest[2]}"
    return data, url

def trip(origin, destination, vehicle):
    orig = geocoding(origin, KEY)
    print(orig)
    dest = geocoding(destination, KEY)
    print(dest)
    if orig[0] == 200 and dest[0] == 200:
        return routing_function(orig, dest, vehicle)
    

def search_place(place):
    params = {
        "q": place,
        "key": KEY
    }
    geo_url = "https://graphhopper.com/api/1/geocode"
    response = requests.get(geo_url, params=params)

    if response.status_code == 200:
        data = response.json()
        locations = [{"name": location["name"], "lat": location["point"]["lat"], "lng": location["point"]["lng"]} for location in data["hits"]]
        return locations
    else:
        return []