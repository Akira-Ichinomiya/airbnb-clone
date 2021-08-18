from django.utils import timezone
from django.views.generic import ListView
from . import models


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
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
