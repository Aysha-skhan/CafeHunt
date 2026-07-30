from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from dotenv import load_dotenv
import os
import requests
load_dotenv()
from .models import Cafe
api_key = os.environ["GOOGLE_API_KEY"]
# Create your views here.
# def search(request):
#     return HttpResponse("Hello, CafeHunt")
def search(request):
    search_lat,search_lng=31.47462066215001, 74.38015766546623
    # search_lat = 31.5186      # hardcoded for now
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
        cafe_dict={"name":cafe.name,"address":cafe.address,"rating":cafe.rating}
        results.append(cafe_dict)
    return JsonResponse(results, safe=False)

