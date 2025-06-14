# Generated by Django 3.1.12 on 2025-03-25 03:09

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(default='Unknown', max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('price', models.FloatField()),
                ('stock', models.IntegerField(default=0)),
                ('thumbnail', models.URLField(blank=True, null=True)),
                ('images', djongo.models.fields.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rate', models.FloatField(default=0)),
                ('rate_count', models.IntegerField(default=0)),
            ],
        ),
    ]
