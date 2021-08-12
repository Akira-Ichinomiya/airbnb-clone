import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed.seeder import Seeder
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "가짜 Rooms 생성함"

    def add_arguments(self, parser):

        parser.add_argument("--number", default=1, type=int, help="가짜 Rooms 생성")

    def handle(self, *args, **options):

        seeder = Seed.seeder()
        number = options.get("number")
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        houserules = room_models.HouseRule.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(0, 300),
                "beds": lambda x: random.randint(0, 5),
                "bedrooms": lambda x: random.randint(0, 5),
                "baths": lambda x: random.randint(0, 5),
                "guests": lambda x: random.randint(1, 6),
            },
        )
        created_rooms = seeder.execute()  # 랜덤한 pk값 얻음 -> 방금 seeder를 통해 생성한 방이 갖는 pk값
        created_clean = flatten(
            list(created_rooms.values())
        )  # flatten을 통해 이중배열안에 있는 배열의 값을 얻음
        for pk in created_clean:
            new_room = room_models.Room.objects.get(
                pk=pk
            )  # pk값과 일치한 방 (방금 만든 seed_room)을 얻어옴
            for i in range(3, random.randint(10, 30)):  # 해당 방에 사진을 랜덤으로 부여
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    file=f"room_photos/{random.randint(1,32)}.webp",
                    room=new_room,
                )

            for a in amenities:  # amenity 랜덤하게 부여
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    new_room.amenities.add(a)

            for f in facilities:  # facility 랜덤하게 부여
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    new_room.facilities.add(f)

            for r in houserules:  # houserules 랜덤하게 부여
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    new_room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} Room(s) created"))
