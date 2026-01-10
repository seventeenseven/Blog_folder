from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from articles.models import Article

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm   #username, email, password1, password2:confirmpassword
    template_name = 'signup.html'
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        #Create user in db
        response = super().form_valid(form)   #super()  => CreateView
        #Login
        user = form.instance
        login(self.request, user)  #Create user session 
        return response

class ProfileView(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        #Récupère le contexte d'origine
        ctx = super().get_context_data(**kwargs)    #super() => TemplateView
        #Récupération de l'utilisateur connecté
        user_obj = self.request.user

        #Récupérer les articles écrits par l'utilisateur
        articles_user = Article.objects.filter(auteur=user_obj)

        #Rajouter les données dans le contexte
        ctx.update({
            "user": user_obj,
            "mes_articles" : articles_user,
            "liked_articles" : []
        })

        return ctx
