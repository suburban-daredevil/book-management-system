# Generated by Django 3.1.4 on 2020-12-24 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BooksApp', '0005_customer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='phone',
        ),
    ]
