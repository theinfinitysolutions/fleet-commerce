from django.urls import path

from .views import AuthenticatedUserView, CustomAuthToken, LogoutView, RegisterView, UserView, DocumentDetailsViewSet, BankDetailsViewSet, OrganizationViewSet, OrganizationRoleViewSet

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("auth-token/", CustomAuthToken.as_view(), name="auth-token"),
    path("user/", AuthenticatedUserView.as_view(), name="authenticated-user"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", UserView.as_view(), name="users"),
    path("document-details/", DocumentDetailsViewSet.as_view(), name="document-details"),
    path("document-details/<int:pk>/", DocumentDetailsViewSet.as_view(), name="document-detail"),
    path("bank-details/", BankDetailsViewSet.as_view(), name="bank-details"),
    path("bank-details/<int:pk>/", BankDetailsViewSet.as_view(), name="bank-detail"),
    path("organizations/", OrganizationViewSet.as_view(), name="organizations"),
    path("organizations/<int:pk>/", OrganizationViewSet.as_view(), name="organization-detail"),
    path("roles/", OrganizationRoleViewSet.as_view(), name="roles"),
    path("roles/<int:pk>/", OrganizationRoleViewSet.as_view(), name="role-detail"),
    path("permissions/", OrganizationRoleViewSet.as_view(), name="permissions"),
    path("permissions/<int:pk>/", OrganizationRoleViewSet.as_view(), name="permission-detail"),
]
