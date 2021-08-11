from django.core.management.base import BaseCommand
from django_seed.seeder import Seeder
from users.models import User
from django_seed import Seed


class Command(BaseCommand):

    help = "가짜 Users 생성함"

    def add_arguments(self, parser):

        parser.add_argument("--number", default=1, type=int, help="가짜 Users 생성")

    def handle(self, *args, **options):

        seeder = Seed.seeder()
        number = options.get("number")
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} User(s) created"))
