import requests
import osmnx as ox

def get_bound(place):
    try:
        gdf = ox.geocode_to_gdf(place)
        bounds = gdf.total_bounds
        return bounds
    except TypeError:
        return None


def get_place_suggestion(query):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "addressdetails": 1,    
        "limit": 5
    }

    if query:
        bounds = get_bound(query)
        if bounds is not None:
            west, south, east, north = bounds
            params["viewbox"] = f"{west},{south},{east},{north}"
            params["bounded"] = 1

    # get request to Nominatim API
    response = requests.get(url, params=params,headers={"User-Agent": "MyApp"})
    if response.status_code == 200:
        suggestions = response.json()
        # for s in suggestions:
        #     print(s['display_name'])

        return [(s['display_name'], (float(s['lat']), float(s['lon']))) for s in suggestions]
    else:
        return []
    

# suggestions = get_bound("Indore")