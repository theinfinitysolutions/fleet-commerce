# Generated by Django 3.2.25 on 2024-05-18 07:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20240518_0553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(choices=[('super_admin', 'super_admin'), ('organisation_admin', 'organisation_admin'), ('vendor', 'vendor')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='role',
            index=models.Index(fields=['name'], name='accounts_ro_name_183ba5_idx'),
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(through='accounts.UserRole', to='accounts.Role'),
        ),
    ]
