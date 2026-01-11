from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeView, PostListView, AboutView, \
            PostDetailView, CommentCreateView, show_categories, \
            ArticleViewSet, supprimer_article, create_article

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
#router.register(r'users', UserViewset)


urlpatterns = [
    path('api/', include(router.urls)),
    path("", HomeView.as_view(), name="home"),
    path("articles/", PostListView.as_view(), name="articles-list"),
    path('about/', AboutView.as_view(), name="about"),
    path("article/<int:pk>/details", PostDetailView.as_view(), name="post-detail"),
    #article/1/details
    #article/2/details
    path("article/<int:pk>/comment", CommentCreateView.as_view(), name="comment-create"),
    path("all_categories/", show_categories, name="all_categories"),
    path('article/<str:article_title>/delete', supprimer_article, name="supprimer_article"),
    path('article/create', create_article, name="article-create"),
]
