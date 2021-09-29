from django.utils import timezone
from django.forms.fields import NullBooleanField
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView
from users import mixins as user_mixins
from . import models, forms


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 12
    ordering = "created"
    paginate_orphans = 3
    page_kwarg = "page"
    context_object_name = "rooms"
    template_name = "rooms/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    """Room Edit Definition"""

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class SearchView(View):

    """SearchView Definition"""

    def get(self, request):

        city = request.GET.get("city")
        print("city=", city)
        if city:

            form = forms.SearchForm(request.GET)
            print(form.is_valid())

            if form.is_valid():
                city = form.cleaned_data.get("city")
                # country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                # filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            print("else가 작동")
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user

    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "사진의 소유자가 아닙니다. 파일을 삭제할 수 없습니다.")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "사진이 삭제되었습니다.")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    fields = ("caption",)
    success_url = "rooms:photos"
    success_message = "성공적으로 업데이트 되었습니다."

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        print(room_pk)
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        messages.success(self.request, "사진이 추가되었습니다.")
        form.save(pk)
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):

        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()
        messages.success(self.request, "방을 생성하였습니다.")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
