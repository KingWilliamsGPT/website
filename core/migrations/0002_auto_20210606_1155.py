# Generated by Django 3.2 on 2021-06-06 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(null=True, upload_to='blog_images'),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.PositiveBigIntegerField(blank=True, editable=False),
        ),
    ]
