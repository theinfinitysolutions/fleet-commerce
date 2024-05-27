# Generated by Django 3.2.25 on 2024-05-04 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_auto_20240504_0525'),
        ('accounts', '0002_auto_20240428_0551'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AddField(
            model_name='user',
            name='aadhar_number',
            field=models.CharField(max_length=12, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='pan_number',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=17, null=True),
        ),
        migrations.CreateModel(
            name='DocumentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('document_type', models.CharField(max_length=100, null=True)),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='utils.fileobject')),
                ('linked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BankDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('bank_account_holder_name', models.CharField(max_length=100, null=True)),
                ('bank_account_number', models.CharField(max_length=18, null=True)),
                ('ifsc_code', models.CharField(max_length=11, null=True)),
                ('bank_name', models.CharField(max_length=100, null=True)),
                ('branch_name', models.CharField(max_length=100, null=True)),
                ('linked_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
