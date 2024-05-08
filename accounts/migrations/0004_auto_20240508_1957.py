# Generated by Django 3.2.25 on 2024-05-08 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizationrole',
            name='permissions',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.CreateModel(
            name='OrganizationPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('permission', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.organizationrole')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
