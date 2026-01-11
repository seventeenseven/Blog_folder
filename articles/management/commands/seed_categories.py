# articles/management/commands/seed_taxonomy.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
import random
import string

from articles.models import Categorie, Tags

CATEGORIES_POOL = [
    "Technologie", "Science", "Éducation", "Voyage", "Cuisine",
    "Santé", "Sport", "Culture", "Business", "Finance",
    "Art", "Musique", "Littérature", "Cinéma", "Nature", "Politique"
]

TAGS_POOL = [
    "python", "django", "ai", "ml", "data", "web", "api", "react", "cloud", "docker",
    "postgres", "linux", "windows", "macos", "devops",
    "security", "testing", "performance", "network", "algorithms",
    "ux", "ui", "design", "tutorial", "guide",
    "tips", "best-practices", "beginner", "advanced", "news",
    "feature", "release", "bugfix", "opensource", "community",
]

def uniq_suffix(n=4):
    return "-" + "".join(random.choices(string.ascii_lowercase + string.digits, k=n))

class Command(BaseCommand):
    help = "Seed des catégories et tags. Idempotent (utilise get_or_create)."

    def add_arguments(self, parser):
        parser.add_argument("--categories", type=int, default=10, help="Nombre de catégories à créer")
        parser.add_argument("--tags", type=int, default=30, help="Nombre de tags à créer")

    @transaction.atomic
    def handle(self, *args, **options):
        n_cat = options["categories"]
        n_tag = options["tags"]

        created_cat = 0
        created_tag = 0

        # ---- Catégories ----
        pool = list(CATEGORIES_POOL)
        while len(pool) < n_cat:
            # recycle en ajoutant un suffixe unique
            base = random.choice(CATEGORIES_POOL)
            pool.append(base + uniq_suffix())

        for name in pool[:n_cat]:
            # Comme ton modèle Categorie a un champ `nom`, on se base dessus.
            obj, was_created = Categorie.objects.get_or_create(nom=name)
            if was_created:
                created_cat += 1

        # ---- Tags ----
        tpool = list(TAGS_POOL)
        while len(tpool) < n_tag:
            base = random.choice(TAGS_POOL)
            # éviter des doublons probables
            tpool.append(base + uniq_suffix())

        for name in tpool[:n_tag]:
            obj, was_created = Tags.objects.get_or_create(nom=name)
            if was_created:
                created_tag += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"OK: Catégories créées: {created_cat}/{n_cat} | Tags créés: {created_tag}/{n_tag}"
            )
        )
