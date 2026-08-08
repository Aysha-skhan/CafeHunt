from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from dotenv import load_dotenv
import os
import requests
load_dotenv()
from .models import Cafe
import math
api_key = os.environ["GOOGLE_API_KEY"]
# Create your views here.
# def search(request):
#     return HttpResponse("Hello, CafeHunt")
def search(request):
    bad_request=HttpResponse("lat and lng are required and must be valid numbers.", status=400) 
    search_lat=request.GET.get("lat")
    search_lng=request.GET.get("lng")
    if (search_lat is None) or (search_lng is None):
        return bad_request  
    try:
        search_lat=float(search_lat)
        search_lng=float(search_lng)
    except (ValueError, TypeError):
            return bad_request
    # search_lat = 31.5186      # hardcoded 
    # search_lng = 74.34589
    nearby = Cafe.objects.filter(
    latitude__lte = search_lat + 0.0045,
    latitude__gte = search_lat - 0.0045,
    longitude__lte = search_lng + 0.0045,
    longitude__gte = search_lng - 0.0045,
)
    if not nearby.exists():
        search_url = "https://places.googleapis.com/v1/places:searchNearby"
        search_headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "places.id,places.displayName,places.location,places.rating,places.formattedAddress",
        }
        body = {
            "includedTypes": ["cafe"],
            "maxResultCount": 4,
            "locationRestriction": {
                "circle": {
                    "center": {"latitude": search_lat, "longitude": search_lng},
                    "radius": 500.0,
                }
            },
        }

        search_response = requests.post(search_url, headers=search_headers, json=body)
        places = search_response.json()["places"]
        for place in places:
            obj, created = Cafe.objects.get_or_create(
            place_id=place["id"],
            defaults={"name":place["displayName"]["text"], "latitude":place["location"]["latitude"],"longitude":place["location"]["longitude"],
                    "rating":place.get("rating"), "address":place.get("formattedAddress")},
        )
    nearby = Cafe.objects.filter(
        latitude__lte = search_lat + 0.0045,
        latitude__gte = search_lat - 0.0045,
        longitude__lte = search_lng + 0.0045,
        longitude__gte = search_lng - 0.0045,
    )

    results = []
    for cafe in nearby:
        # distance calculation
        routes_url="https://routes.googleapis.com/directions/v2:computeRoutes"
        routes_body={
            "origin":{
                "location":{
                "latLng":{
                    "latitude": search_lat,
                    "longitude": search_lng
                }
                }
            },
            "destination":{
                "location":{
                "latLng":{
                    "latitude": cafe.latitude,
                    "longitude": cafe.longitude
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
        distance_km = ans['routes'][0]['distanceMeters'] / 1000
        distance_km = round(distance_km, 1)

        duration_minutes = math.ceil(
            int(ans['routes'][0]['duration'].replace('s', '')) / 60
        )

        cafe_dict={"name":cafe.name,"address":cafe.address,"rating":cafe.rating,"distance":distance_km,"time to reach by car":duration_minutes}
        results.append(cafe_dict)
    return JsonResponse(results, safe=False)
    

