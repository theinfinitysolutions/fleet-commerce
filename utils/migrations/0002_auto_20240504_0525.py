# Generated by Django 3.2.25 on 2024-05-04 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileobject',
            name='mime_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fileobject',
            name='original_file_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fileobject',
            name='s3_bucket',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fileobject',
            name='s3_key',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fileobject',
            name='size',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
    ]