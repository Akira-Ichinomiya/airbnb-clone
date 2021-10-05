from . import forms
from rooms import models as room_models
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

# Create your views here.
def create_review(request, room):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            messages.error(request, "잘못된 경로입니다.")
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, "리뷰가 작성되었습니다.")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
        else:
            messages.error(request, "리뷰를 작성하는데 실패했습니다.")
            return redirect(reverse("core:home"))
