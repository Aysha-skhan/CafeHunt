from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
api_key = os.environ["GOOGLE_API_KEY"]

search_url = "https://places.googleapis.com/v1/places:searchNearby"
search_headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": api_key,
    "X-Goog-FieldMask": "places.id,places.displayName",
}
body = {
    "includedTypes": ["cafe"],
    "maxResultCount": 4,
    "locationRestriction": {
        "circle": {
            "center": {"latitude": 31.5186, "longitude": 74.34589},
            "radius": 500.0,
        }
    },
}

search_response = requests.post(search_url, headers=search_headers, json=body)
places = search_response.json()["places"]

details_headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": api_key,
    "X-Goog-FieldMask": "displayName,outdoorSeating",
}

for place in places:
    place_id = place["id"]
    details_url = f"https://places.googleapis.com/v1/places/{place_id}"
    details_response=requests.get(details_url, headers=details_headers)
    details_data=details_response.json()
    outdoor = details_data.get("outdoorSeating")
    display_name = details_data["displayName"]["text"]
    if display_name:
        print("Name of the Cafe is: ",display_name)
    if outdoor is True:
        print("✅ Outdoor seating: Yes")
    elif outdoor is False:
        print("❌ Outdoor seating: No")
    else:
        print("❓ Outdoor seating: Unknown (field missing)")

routes_url="https://routes.googleapis.com/directions/v2:computeRoutes"
routes_body={
  "origin":{
    "location":{
      "latLng":{
        "latitude": 31.51945284553336,
        "longitude": 74.3456551851925
      }
    }
  },
  "destination":{
    "location":{
      "latLng":{
        "latitude": 31.53262038426561,
        "longitude": 74.3605894759086
      }
    }
  },
  "travelMode": "DRIVE",
  "routingPreference": "TRAFFIC_AWARE",
  "computeAlternativeRoutes": False,
  "routeModifiers": {
    "avoidTolls": False,
    "avoidHighways": False,
    "avoidFerries": False
  },
  "languageCode": "en-US",
  "units": "METRIC"
}
routes_headers={"Content-Type": "application/json","X-Goog-Api-Key":api_key,
"X-Goog-FieldMask": "routes.distanceMeters,routes.duration"}

routes_response = requests.post(routes_url, headers=routes_headers, json=routes_body)
ans = routes_response.json()
print(ans)
