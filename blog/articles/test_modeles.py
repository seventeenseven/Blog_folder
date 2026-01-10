from django.test import TestCase
from articles.models import Article, Categorie, Tags, Commentaire
from django.contrib.auth.models import User


class ArticleModeleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@mail.com", "pass")
        self.categorie = Categorie.objects.create(nom="Test")
        self.tag = Tags.objects.create(nom = "testtag")


    def test_creation_article(self):
        # Fact - Act - Assert
        #ACT
        my_article = Article.objects.create(
            titre= "Mon Article",
            contenu="Texte",
            categorie = self.categorie,
            auteur = self.user
        )
        my_article.tags.add(self.tag)
        #ASSERT
        self.assertEqual(my_article.titre,"Mon Article")
        self.assertEqual(my_article.tags.count(), 1)
        self.assertNotEqual(my_article.contenu, "Hello")


class CommentaireTest(TestCase):
    def test_create_comment_and_article_relation(self):
        #Fact
        user = User.objects.create_user("testuser", "test@mail.com", "pass")
        cat = Categorie.objects.create(nom="Test")
        tag = Tags.objects.create(nom = "testtag")
        art = Article.objects.create(titre="test", contenu="...", categorie=cat, auteur=user)
        #Act
        comment = Commentaire.objects.create(
            contenu="test",
            name ="UserTest",
            article = art
        )
        #Assert
        #self.assertEqual(comment.article_id, art.id)
        self.assertEqual(comment.article.titre, art.titre)
        self.assertNotEqual(comment.name, art.auteur.username)
        self.assertEqual(comment.contenu, "test")



