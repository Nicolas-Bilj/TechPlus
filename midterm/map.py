import requests
import urllib.parse

KEY = "473cdd1a-6274-4cf4-8485-2ca79a23d1c9"

def geocoding(location, key):
    """
    Get the latitude and longitude of a location using the GraphHopper Geocoding API.

    Parameters:
        location (str): The location to geocode.
        key (str): The API key for GraphHopper.

    Returns:
        int: The status code of the API request.
        float: The latitude of the location.
        float: The longitude of the location.
        str: The name of the location.
    """
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

def routing_function(orig, dest, vehicle):
    """
    Get the route between two locations using the GraphHopper Routing API.

    Parameters:
        orig (tuple): The origin location as a tuple of latitude and longitude.
        dest (tuple): The destination location as a tuple of latitude and longitude.
        vehicle (str): The vehicle type for routing.

    Returns:
        dict: The route data.
    """
    route_url = "https://graphhopper.com/api/1/route?"
    op="&point="+str(orig[1])+"%2C"+str(orig[2])
    dp="&point="+str(dest[1])+"%2C"+str(dest[2])
    paths_url = route_url + urllib.parse.urlencode({"key":KEY, "vehicle":vehicle}) + op + dp
    paths_status = requests.get(paths_url).status_code
    paths_data = requests.get(paths_url).json()
    print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
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
    for instruction in data['instructions']:
        instruction['distance'] = int(round(instruction['distance'], 0))
    #get openStreetMap url using the instructions as one road
    if vehicle == "bike":
        vehicle = "bicycle"
    url = f"https://www.openstreetmap.org/directions?engine=graphhopper_{vehicle}&route={orig[1]}%2C{orig[2]}%3B{dest[1]}%2C{dest[2]}"
    return data, url

def trip(origin, destination, vehicle):
    """
    Get the route between two locations using the GraphHopper Geocoding and Routing APIs.

    Parameters:
        origin (str): The origin location.
        destination (str): The destination location.
        vehicle (str): The vehicle type for routing.

    Returns:
        dict: The route data.
    """
    orig = geocoding(origin, KEY)
    print(orig)
    dest = geocoding(destination, KEY)
    print(dest)
    if orig[0] == 200 and dest[0] == 200:
        return routing_function(orig, dest, vehicle)
    

def search_place(place):
    """
    Search for a place using the GraphHopper Geocoding API.

    Parameters:
        place (str): The place to search for.

    Returns:
        list: A list of locations matching the search query.
    """
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