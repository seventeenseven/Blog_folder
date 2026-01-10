from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class nom_modele_de_donnée(models.Model)

class Tags(models.Model):
    nom = models.CharField(max_length=100)

class Article(models.Model):            #Sera traduit en table de donnée
    #Définir les attributs
    #Ces attributs constitueront les colonnes de ma table Article

    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    #One to Many
    categorie = models.ForeignKey("Categorie", on_delete=models.CASCADE)
    #One to one
    #image_principal = models.OneToOneField("ImagePrincipale", on_delete=models.DO_NOTHING)
    #Many to Many
    tags = models.ManyToManyField(Tags, related_name="articles")

    #Relation entre les articles et les utilisateurs (auteurs)
    auteur = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    #Si je rajoute un nouveau champ dans un modèle existant, je dois le rendre optionnel avec blank=True
    # soustitre = models.CharField(max_length=100, blank=True, null=True)

    #Rajouter des options supplementaires avec la classe Meta
    class Meta :
        permissions = [
            ("peut_modifier_article", "Peut modifier article"),
            ("peut_supprimer_article", "Peut supprimer article")
        ]

    def __str__(self):
        return f'Article : {self.titre}'


class Categorie(models.Model):
    nom = models.CharField()

    def __str__(self):
        return self.nom
    
class Commentaire(models.Model):
    contenu = models.TextField()
    name = models.CharField(max_length=100)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_publication = models.DateTimeField(auto_now_add=True)

class Photo(models.Model):
    image = models.ImageField(upload_to="articles/%Y/%m/%d")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="photos")
    legende = models.CharField(max_length=255, blank=True)  #optionnel
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo de l'article {self.article.titre}"

