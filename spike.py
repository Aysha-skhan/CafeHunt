from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
api_key = os.environ["GOOGLE_API_KEY"]

# --- Step 1: Nearby Search to get a list of café ids ---
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

# --- Step 2: for each café, call Place Details and check outdoorSeating ---
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

    # YOUR TASK — write the body of this loop:
    # 1. GET the details_url with details_headers
    # 2. parse the JSON
    # 3. read the name (displayName.text) and outdoorSeating SAFELY
    #    (remember: use .get() so a missing field gives None instead of crashing)
    # 4. print the name and what outdoorSeating came back as