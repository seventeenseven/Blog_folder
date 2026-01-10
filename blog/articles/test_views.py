from django.test import TestCase
from articles.models import Article, Categorie, Tags, Commentaire
from django.contrib.auth.models import User
from django.urls import reverse

class CommentCreateViewsTest(TestCase):
    def test_post_comment(self):
        #Fact
        user = User.objects.create_user("testuser", "test@mail.com", "pass")
        cat = Categorie.objects.create(nom="Test")
        tag = Tags.objects.create(nom = "testtag")
        art = Article.objects.create(titre="test", contenu="...", categorie=cat, auteur=user)
        #Act
        url = reverse("comment-create", kwargs={"pk": art.pk})
        #HTTP request
        response = self.client.post(url,  data={"name":"harry", "contenu":"Test comment"}, follow=True)

        #Assertion
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "Test")
        self.assertEqual(art.commentaire_set.count(), 1)



