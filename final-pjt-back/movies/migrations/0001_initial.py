# Generated by Django 4.2.4 on 2023-11-21 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('overview', models.TextField(blank=True, null=True)),
                ('poster_path', models.CharField(max_length=50)),
                ('released_date', models.CharField(max_length=50)),
                ('popularity', models.FloatField()),
                ('vote_count', models.IntegerField()),
                ('vote_average', models.FloatField()),
                ('creater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_movies', to=settings.AUTH_USER_MODEL)),
                ('genre', models.ManyToManyField(blank=True, related_name='genre_movies', to='movies.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_score', models.FloatField()),
                ('rate_movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('rate_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_rated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='rates_users',
            field=models.ManyToManyField(related_name='user_rated_movie', through='movies.Rate', to=settings.AUTH_USER_MODEL),
        ),
    ]