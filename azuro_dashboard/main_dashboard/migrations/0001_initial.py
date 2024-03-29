# Generated by Django 3.1.13 on 2023-11-22 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardRows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant_name', models.CharField(max_length=200, verbose_name='Participant name')),
                ('points', models.IntegerField(verbose_name='Points')),
            ],
            options={
                'verbose_name': 'Dashboard row',
                'verbose_name_plural': 'Dashboard rows',
                'db_table': 'dashboard_dashboardrows',
            },
        ),
    ]
