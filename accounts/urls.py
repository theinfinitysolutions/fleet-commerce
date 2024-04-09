from django.urls import path

from .views import AuthenticatedUserView, CustomAuthToken, LogoutView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("auth-token/", CustomAuthToken.as_view(), name="auth-token"),
    path("user/", AuthenticatedUserView.as_view(), name="authenticated-user"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
