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

    destinations = []
    for cafe in nearby:
        # distance calculation
        destinations.append({"waypoint": {"location": {"latLng": {"latitude": cafe.latitude, "longitude": cafe.longitude}}}})
        origins = [{"waypoint": {"location": {"latLng": {"latitude": search_lat, "longitude": search_lng}}}}]

    matrix_url = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
    matrix_headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "originIndex,destinationIndex,distanceMeters,duration",
    }
    matrix_body = {
        "origins": origins,             # your list from piece one
        "destinations": destinations,   # your list from piece one
        "travelMode": "DRIVE",
    }

    matrix_response = requests.post(matrix_url, headers=matrix_headers, json=matrix_body)
    matrix_data = matrix_response.json()
    # print(matrix_data)   # <-- we're going to LOOK at this before using it
    route_by_index = {}
    for element in matrix_data:
        idx = element["destinationIndex"]
        route_by_index[idx] = element      # now route_by_index[2] gives destination 2's result
    results = []
    for index, cafe in enumerate(nearby):
        route = route_by_index[index]          # this café's route, by position
        distance_km = round(route["distanceMeters"] / 1000, 1)
        duration_minutes = math.ceil(int(route["duration"].replace("s","")) / 60)
        cafe_dict = {"name": cafe.name, "address": cafe.address, "rating": cafe.rating,
                    "distance": distance_km, "time to reach by car": duration_minutes}
        results.append(cafe_dict)
    return JsonResponse(results, safe=False)

# maxResultCount kept at 4 for now — trivial to raise later, not worth tuning mid-build.
# Known limitation: cache serves the same set for any point within ~0.0045°, so
# results aren't precise per-point. Proper fix (precise per-point queries) = PostGIS/GeoDjango.
# Note: count and spatial indexing are SEPARATE concerns — PostGIS won't remove the need to pick a count.

def home(request):
    return render(request, "home.html")