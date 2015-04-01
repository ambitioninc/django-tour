# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('display_name', models.CharField(max_length=128)),
                ('url', models.CharField(max_length=128, blank=True, null=True)),
                ('step_class', models.CharField(max_length=128, unique=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('parent_step', models.ForeignKey(related_name='steps', null=True, to='tour.Step')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('display_name', models.CharField(max_length=128)),
                ('tour_class', models.CharField(max_length=128, unique=True)),
                ('complete_url', models.CharField(max_length=128, blank=True, null=True, default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TourStatus',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('complete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('complete_time', models.DateTimeField(blank=True, null=True, default=None)),
                ('tour', models.ForeignKey(to='tour.Tour')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tour',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='tour.TourStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='step',
            name='tour',
            field=models.ForeignKey(to='tour.Tour', related_name='steps'),
            preserve_default=True,
        ),
    ]
