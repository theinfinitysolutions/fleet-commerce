from django.urls import path

from .views import (
    AuthenticatedUserView,
    BankDetailsView,
    CustomAuthToken,
    DocumentDetailsView,
    LogoutView,
    RegisterView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("auth-token/", CustomAuthToken.as_view(), name="auth-token"),
    path("user/", AuthenticatedUserView.as_view(), name="authenticated-user"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("bank-detail/<int:pk>/", BankDetailsView.as_view(), name="purchase-detail"),
    path("bank-detail/", BankDetailsView.as_view(), name="purchase-create"),
    path("document-detail/<int:pk>/", DocumentDetailsView.as_view(), name="document-detail"),
    path("document-detail/", DocumentDetailsView.as_view(), name="document-create"),
]
