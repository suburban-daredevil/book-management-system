# Generated by Django 3.1.4 on 2020-12-23 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BooksApp', '0002_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='BooksApp.customer'),
        ),
    ]
