import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from django_seed.seeder import Seeder
from lists import models as list_models
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "가짜 lists 생성함"

    def add_arguments(self, parser):

        parser.add_argument("--number", default=1, type=int, help="가짜 list 생성")

    def handle(self, *args, **options):

        seeder = Seed.seeder()
        number = options.get("number")
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        print(rooms)
        seeder.add_entity(
            list_models.List,
            number,
            {
                "name": lambda x: seeder.faker.sentence(nb_words=3),
                "user": lambda x: random.choice(users),
            },
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(5, 30)]
            list_model.rooms.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"{number} list(s) created"))
