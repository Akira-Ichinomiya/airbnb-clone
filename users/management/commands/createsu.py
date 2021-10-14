from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):

    help = "가짜 su 생성함"

    def handle(self, *args, **options):
        User = get_user_model()
        admin = User.objects.get_or_none(username="ebadmin")
        if not admin:
            User.objects.create_superuser("ebadmin", "tkmt123@nate.com", "123123")
            self.stdout.write(self.style.SUCCESS("superuser created"))
        else:
            self.stdout.write(self.style.SUCCESS("superuser already exists."))
