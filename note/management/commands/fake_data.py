from django.core.management.base import BaseCommand
from faker import Faker
import random

from note.models import Note, Tag, Media


class Command(BaseCommand):
    help = "Génère de fausses données pour Note, Tag et Media"

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write("Création des tags...")
        tags = []
        for _ in range(5):
            tag = Tag.objects.create(
                nom_tag=fake.word()
            )
            tags.append(tag)

        self.stdout.write("Création des notes et médias...")
        for _ in range(10):
            note = Note.objects.create(
                titre=fake.sentence(nb_words=4),
                contenu=fake.text(max_nb_chars=300),
            )

            selected_tags = random.sample(tags, k=random.randint(1, min(3, len(tags))))
            note.tags.set(selected_tags)

            Media.objects.create(
                note=note,
                type='lien',
                url=fake.url()
            )

        self.stdout.write(self.style.SUCCESS("Fausses données créées avec succès !"))