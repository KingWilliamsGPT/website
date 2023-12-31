# Generated by Django 3.2 on 2021-06-07 03:19

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210607_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(default=core.models.slug),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_when', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(blank=True, default='anonymous', max_length=150)),
                ('comment_text', models.CharField(max_length=3000)),
                ('author', models.ForeignKey(limit_choices_to=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('blog', models.ForeignKey(limit_choices_to=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.blog')),
            ],
            options={
                'ordering': ['-created_when'],
                'abstract': False,
            },
        ),
    ]
