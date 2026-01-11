from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import SignUpView, ProfileView

app_name='users'

urlpatterns= [
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup', SignUpView.as_view(), name="signup"),
    path('profile/', ProfileView.as_view(), name='profile'),
]
