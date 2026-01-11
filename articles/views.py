from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .forms import CommentCreateForm
from .models import Article, Commentaire, Categorie
import datetime
from django.db.models import Q, Count
from django.contrib.auth.models import User

from rest_framework import viewsets
from .serializers import ArticleSerializer
from django.contrib.auth.decorators import permission_required

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

class PostListView(ListView): 
    model = Article  #Article.objects.all()
    template_name = "post_list.html"
    context_object_name = "articles"   #return render(request, template, context)
    paginate_by = 5
    permission_required = 'articles.delete_article'

class AboutView(TemplateView):
    template_name = "about.html"  

class PostDetailView(DetailView):
    model = Article
    template_name = "article-detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = CommentCreateForm()  # <- objet formulaire pour le template
        return ctx

class CommentCreateView(CreateView):
    model = Commentaire
    #fields = ["name", "contenu"]
    form_class = CommentCreateForm
    context_object_name = "form"

    def form_valid(self, form):
        form.instance.article_id = self.kwargs['pk'] # Associer le commentaire à l'article
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']}) # Rediriger vers l'article après soumission


#Vues basées sur les fonctions
"""
Vue pour afficher toutes les categories
"""
def show_categories(request):
    #récupération des categories de la bd : ModelName.objects.all()
    categories = Categorie.objects.all()   #retourne un query set, une liste d'objets
    return render(request, "categories.html", {"categories_list": categories})


"""
Vue pour afficher les articles et les informations de l'auteur
"""
def list_articles_author(request):
    articles_authors_info = Article.objects.select_related('auteur').all()

    date_hier = datetime.datetime.today() - datetime.timedelta(days=1)       
    articles_today = Article.objects.filter(date_publication__gt= date_hier) 

    articles_jane_avanthier = Article.objects.filter(Q(auteur__username="jane") 
                                & Q(date_publication__lte =date_hier))\
                                .order_by('-titre')
    total_articles_jane = len(Article.objects.filter(auteur__username='jane'))
    total_articles_per_author = User.objects.annotate(article_count = Count('article'))
    return render(request, 'article_auteurs.html', {"infos": articles_authors_info})

@permission_required('articles.peut_supprimer_article', raise_exception=True)
def supprimer_article(request, article_title):
    #article = Article.objects.filter(pk=article_id).first() #si Id n'existe pas, alors article sera None, article.titre , None.titre
    #article = Article.objects.get(pk=article_id)
    article = get_object_or_404(Article, titre=article_title)
    article.delete()
    return redirect("articles-list")


#-------------------------- DJANGO REST
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    