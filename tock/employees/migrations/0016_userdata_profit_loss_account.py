# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 19:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_remove_profitlossaccount_as_active'),
        ('employees', '0015_auto_20161006_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='profit_loss_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.ProfitLossAccount'),
        ),
    ]
