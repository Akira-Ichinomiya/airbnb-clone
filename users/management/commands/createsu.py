from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "가짜 su 생성함"

    def handle(self, *args, **options):

        admin = User.objects.get_or_none(username="ebadmin")
        if not admin:
            User.objects.create_superuser("ebadmin", "tkmt123@nate.com", "123123")
            self.stdout.write(self.style.SUCCESS("superuser created"))
        else:
            self.stdout.write(self.style.SUCCESS("superuser already exists."))
