from django.db import models
from django_countries.fields import CountryField
from core import models as core_models


class AbstractItem(core_models.TimeStampedModel):
    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Amenity(AbstractItem):
    """Amenity Model Definition"""

    pass

    class Meta:
        verbose_name_plural = "Amenities"


class RoomType(AbstractItem):

    """RoomType Model Definition"""

    pass


class Meta:
    verbose_name = "Room Type"
    ordering = ["-created"]


class Facility(AbstractItem):

    """Facility Model Definition"""

    pass

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    pass

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


# Create your models here.
class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=144, blank=False, unique=True, default=None)
    description = models.TextField(blank=True)
    country = CountryField()
    city = models.CharField(max_length=80, blank=True)
    price = models.IntegerField()
    address = models.CharField(max_length=140, blank=True)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )  # related_name: rooms를 통해 User가 room을 참조할 수 있음
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", null=True, on_delete=models.SET_NULL
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name
