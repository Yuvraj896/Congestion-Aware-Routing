import requests
import osmnx as ox

# GeoDataFrame gfd

def get_bbox(place):
    try:
        gdf = ox.geocode_to_gdf(place)
        bbox = gdf.total_bounds
        return bbox
    except TypeError:
        return None


def get_place_suggestion(query, place_name=None):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "addressdetails": 1,    
        "limit": 5
    }

    if place_name:
        try:
            bbox = get_bbox(place_name)
            params["viewbox"] = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"
            
            # params["bounded"] = 1 #this forces nominatim to search ONLY in box

        except Exception as e:
            print(f"Error getting viewbox : {e}")

    # get request to Nominatim API
    response = requests.get(url, params=params,headers={"User-Agent": "MyApp"})
    if response.status_code == 200:
        suggestions = response.json()
        # for s in suggestions:
        #     print(s['display_name'])

        return [(s['display_name'], (float(s['lat']), float(s['lon']))) for s in suggestions]
    else:
        return []
    

# suggestions = get_place_suggestion("seoni", "Chhindwara")
# print(suggestions)  