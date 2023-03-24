# Generated by Django 4.1.7 on 2023-03-23 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('name',), 'verbose_name': ('Тег',), 'verbose_name_plural': 'Теги'},
        ),
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique add to favorites'),
        ),
    ]