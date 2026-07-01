from django.db import models

class Cafe(models.Model):
    place_id = models.CharField(max_length=255, unique=True)  # Google's stable id; unique = no duplicates
    name = models.CharField(max_length=255)                    # the extracted displayName.text string
    latitude = models.FloatField()                             # from location.latLng
    longitude = models.FloatField()
    rating = models.FloatField(null=True)                      # nullable: some cafés have no rating yet
    outdoor_seating = models.BooleanField(null=True)           # your 3-state field: True / False / None
    address = models.CharField(max_length=500, blank=True)     # we'll add this from Place Details later
    fetched_at = models.DateTimeField(auto_now=True)           # timestamp; powers the cache freshness check

    def __str__(self):
        return self.name