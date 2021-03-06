from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from django.urls import reverse
from core import models as core_models
from cal import Calendar


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
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


# Create your models here.
class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=144, blank=False, default=None)
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
    )  # related_name: rooms??? ?????? User??? room??? ????????? ??? ??????
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", null=True, on_delete=models.SET_NULL
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return all_ratings / len(all_reviews)
        return 0

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except:
            return None

    def get_next_four_photos(self):
        try:
            photos = self.photos.all()[1:5]
            return photos
        except:
            return None

    def get_calendar(self):
        now = timezone.now()
        year = now.year
        month = now.month
        current_month = Calendar(year, month)
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        next_month = Calendar(year, month)

        return [current_month, next_month]
