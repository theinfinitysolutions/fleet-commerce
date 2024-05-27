from accounts.models import Role


def populate_roles():
    Role.objects.all().delete()
    for role in Role.USER_ROLE_CHOICES:
        Role.objects.get_or_create(name=role[0])
